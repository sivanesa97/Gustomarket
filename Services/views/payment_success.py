"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
import time
from django.shortcuts import render, redirect
from django.contrib import messages
from Services.models import Order, Cart, Notification, OrderItem
from decimal import Decimal
from django.conf import settings
import stripe  # type: ignore
from Services.views.send_mail import send_notification_email
from datetime import datetime, timedelta
from weasyprint import HTML
import pdfkit
import pytz
import os
import random
from decimal import Decimal

stripe.api_key = settings.STRIPE_PUBLIC_KEY


def payment_success(request):
    """
    remove items into the cart for a successful payment.
    """
    order_id = request.session.get('order_id')
    print("Received order id: ", order_id)

    # PDF generation, etc., should really be done on a background thread.
    # Doing this is not worth it for the time being, though, given the overall state of the project.
    if order_id:
        try:
            eastern_time = datetime.now(pytz.timezone('US/Eastern'))

            order = Order.objects.get(orderID=order_id)
            cart_items = Cart.objects.filter(user=order.customer.user)

            for cart_item in cart_items:
                cart_item.delete()

            # Setup buyer email information
            buyer = order.customer.user
            buyer_email = order.customer.email
            buyer_email = buyer_email.strip()

            # Setup invoice & picklist HTML templates
            with open(r"Services/templates/invoice_template.html") as f:
                invoice_html = f.read()
            with open(r"Services/templates/picklist_template.html") as p:
                picklist_html = p.read()
            with open(r"Services/templates/purchase_order_template.html") as po:
                purchase_order_html = po.read()

            # populating the invoice template for invoices
            invoice_html = invoice_html.replace("BUYER_NAME", order.customer.name) \
                .replace("ORDER_ID", order_id) \
                .replace("BUYER_EMAIL", order.customer.email) \
                .replace("BUYER_ADDR_LINE1", order.customer.address.address_lane_1 if order.customer.address else "") \
                .replace("BUYER_CITY", order.customer.address.city if order.customer.address else "") \
                .replace("BUYER_STATE", order.customer.address.state.state_name if order.customer.address else "") \
                .replace("BUYER_ZIP", order.customer.address.zip_code if order.customer.address else "") \
                .replace("CURRENT_DATE", eastern_time.strftime("%B %d, %Y %I:%M %p")) \
                .replace("DUE_DATE", "Aug 15, 2024, 4:00pm") \
                .replace("PAYMENT_TERMS", str(order.payment))

            # populating the Picklist Template for Invoice
            picklist_html = picklist_html.replace("BUYER_NAME", order.customer.name).replace("ORDER_ID",
                                                                                             order_id).replace(
                "ORDER_SEC", order.order_date.strftime("%y%m") + str(order.id)) \
                .replace("BUYER_EMAIL", order.customer.email).replace(
                "BUYER_ADDR_LINE1",
                order.customer.address.address_lane_1 if order.customer.address else "") \
                .replace("BUYER_CITY", order.customer.address.city if order.customer.address else "") \
                .replace("BUYER_STATE", order.customer.address.state.state_name if order.customer.address else "") \
                .replace("BUYER_ZIP", order.customer.address.zip_code if order.customer.address else "")
            picklist_html = picklist_html.replace(
                "CURRENT_DATE", eastern_time.strftime("%B %d, %Y %I:%M %p"))
            picklist_template_parts = picklist_html.split("<!--DATA_GOES_HERE-->")

            # populating the Purchase Order Template for Invoice
            purchase_order_html = purchase_order_html.replace("BUYER_NAME", order.customer.name).replace("ORDER_ID",
                                                                                                         order_id).replace(
                "ORDER_SEC", order_id) \
                .replace("BUYER_EMAIL", order.customer.email).replace("BUYER_ADDR_LINE1",
                                                                      order.customer.address.address_lane_1) \
                .replace("BUYER_CITY", order.customer.address.city) \
                .replace("BUYER_STATE", order.customer.address.state.state_name) \
                .replace("BUYER_ZIP", order.customer.address.zip_code) \
                .replace('BUYER_COMPANY_NAME', order.customer.address.location).replace(
                "SELLER_PHONE", order.customer.phone if order.customer else "Not Available"
            )
            purchase_order_html = purchase_order_html.replace(
                "DUE_DATE", "Aug 15, 2024, 4:00pm")
            purchase_order_html = purchase_order_html.replace(
                "PAYMENT_TERMS", str(order.payment))
            purchase_order_html = purchase_order_html.replace("CURRENT_DATE",
                                                              eastern_time.strftime("%B %d, %Y %I:%M %p"))
            purchase_order_template_parts = purchase_order_html.split("DATA_GOES_HERE")

            # Seller Aggregation for Invoice Generation
            seller_agg = {}
            for prod in order.products.all():
                cur_seller_email = prod.supplier.email
                if cur_seller_email not in seller_agg.keys():
                    seller_agg[cur_seller_email] = {
                        'seller': prod.supplier, 'products': []}
                seller_agg[cur_seller_email]['products'].append(prod)

            # Generate invoices, picklists & send seller emails
            # buyer_invoices = []
            buyer_purchase_orders = []

            # Iterate through the aggregated sellers (two loops instead of one for readability.
            for seller_email in seller_agg.keys():
                products_sold = {}
                for p in seller_agg[seller_email]['products']:
                    if p.product_title not in products_sold.keys():
                        products_sold[p.product_title] = 1
                    else:
                        products_sold[p.product_title] += 1

                # Select relevant order items (affiliated with the current supplier
                order_items = OrderItem.objects.filter(
                    order__orderID=order_id, product__supplier=seller_agg[seller_email]['seller'])
                cur_added_items = set()
                order_total = 0
                cur_picklist_record_data = ""
                cur_invoice_record_data = ""

                # creating order list for purchase orders pdf
                cur_purchaseorder_record_data = f"""

                    <table  style="position: fixed;top:45%; right:0.2%; width: 100%;border-collapse: collapse;">
                                <thead style="margin-right: 75px; background-color: white;">
                                    <tr class="heading" style="padding:2px; padding-left:130px;padding:5px" >
                                        <td class="qt">
                                            <p style="font-weight: bold; color:#555;"><strong>Product</strong></p>

                                        </td>
                                        <td class="qt" style="padding:2px;">
                                            <p style="font-weight: bold; color:#555;margin-left:2px"><strong>Quantity</strong></p>
                                        </td>
                                        <td class="qt" style="padding:2px;">
                                            <p style="font-weight: bold; color:#555; "><strong>Unit Sold</strong></p>
                                        </td> 
                                        <td class="qt" style="text-align: left;" style="padding:2px;">
                                            <p style="font-weight: bold; color:#555; "><strong>Unit price</strong></p>
                                        </td>
                                        <td class="qt" style="padding:2px; ">
                                            <p style="font-weight: bold; color:#555;  "><strong>Unit of Pricing</strong></p>
                                        </td>
                                        <td class="qt" style="text-align: left;"style="padding:2px;">
                                            <p style="font-weight: bold; color:#555;"><strong>Sub Total</strong></p>
                                        </td>
                                    </tr>



                                </thead>

                                """

                for order_item in order_items:
                    product_title = order_item.product.product_title[:15]
                    if len(order_item.product.product_title) > 15:
                        product_title += "..."
                    cur_purchaseorder_record_data += f"""
                            <tr style"position:relative; margin-right: 70px">
                               <td class="qt">
                                    <p>{order_item.product.product_title}</p><p style="font-size: small; color:#606060;">{order_item.product.description}</p>
                               </td>
                                <td class="qt" style="text-align: center;">
                                   <p style="text-align: center;">{order_item.quantity}</p>
                                </td>
                                <td class="qt" style="text-align: center;">
                                   <p style="text-align: center;">{order_item.product.product_packaging.sku_sold}</p>
                                </td>
                                <td class="qt" style="text-align: center; ">
                                    <p>{order_item.total_price}</p>
                               </td>
                                <td class="qt" style="text-align: center;">
                                   <p style="text-align: center; ">{order_item.product.product_packaging.sku_unit}</p>
                                </td>

                               <td class="qt" style="text-align: center;">
                                    <p>${order_item.quantity * order_item.total_price}</p>
                               </td>
                            </tr>
                        """
                cur_purchaseorder_record_data += f"""
                        <!-- DATA GOES HERE -->
                        </tbody>

                    </table>

                    """

                def get_safe_sku_packaged(v):
                    if v is None:
                        return "Standard (Unspecified)"
                    else:
                        if v.selling_option is None:
                            return "Standard (Unspecified)"
                        else:
                            return v.selling_option

                def get_safe_sku_unit(v):
                    if v is None:
                        return "Standard (Unspecified)"
                    else:
                        if v.unit_option is None:
                            return "Standard (Unspecified)"
                        else:
                            return v.unit_option

                # Iterate through order items, generating picklist  records
                for order_item in order_items.all():
                    if order_item.product.product_title in cur_added_items:
                        continue
                    order_total += order_item.total_price * order_item.quantity

                    ##CHANGE 4 7:26PM

                    cur_picklist_record_data += f"""
                                            <tr>
                                                <td style="margin-right:5px;">{order_item.product.product_title}<br>{order_item.product.description}</td>
                                                <td>{order_item.quantity}</td>
                                                <td>{get_safe_sku_packaged(order_item.product.product_packaging.sku_sold)}</td>
                                                <td>
                                                    <label class="checkbox-label" style="margin-left:42px;">
                                                    <input type="checkbox" class="custom-checkbox">
                                                    <span class="checkmark"></span>
                                                    </label>
                                                </td>
                                                <td>
                                                    <label class="checkbox-label"style="margin-left:42px;">
                                                    <input type="checkbox" class="custom-checkbox">
                                                    <span class="checkmark"></span>
                                                    </label>
                                                </td>
                                                <td>
                                                    <label class="checkbox-label"style="margin-left:28px;">
                                                    <input type="checkbox" class="custom-checkbox">
                                                    <span class="checkmark"></span>
                                                    </label>
                                                </td>

                    			            </tr>     
                                           """

                    cur_purchaseorder_record_data += f"""
                        <tr class="item">
                            <td>{order_item.product.product_title}<br><small>{order_item.product.description}</small></td>
                            <td class="qt"><p>{order_item.quantity}</p></td>
                        </tr>
                    """

                    cur_added_items.add(order_item.product.product_title)
                # Prepare seller invoice pdf

                #INVOICE_GEN CHANGE 1
                # cur_seller_invoice_html = invoice_template_parts[0] + \
                #     cur_invoice_record_data + invoice_template_parts[1]
                # cur_seller_invoice_html = cur_seller_invoice_html.replace(
                #     "SELLER_NAME", seller_agg[seller_email]['seller'].first_name + " " + seller_agg[seller_email]['seller'].last_name).replace("SELLER_EMAIL", seller_email)
                # cur_seller_invoice_html = cur_seller_invoice_html.replace("GRAND_TOTAL", str(order_total)).replace(
                #     "SELLER_COMPANY", seller_agg[seller_email]['seller'].company.company_name)

                #saving as a html file --to be fetched in seller_dashboard.py to be converted to pdf
                cur_seller_invoice_file_name = "invoice_" + order_id + "__" + \
                                               order.customer.name.replace(
                                                   " ", "") + "__" + str(time.time()) + ".html"
                cur_seller_html_filepath = os.path.join(
                    settings.MEDIA_ROOT, 'invoices', cur_seller_invoice_file_name)
                order.invoice_filepath = cur_seller_html_filepath
                order.save()
                with open(cur_seller_html_filepath, "w") as html_invoice_file:
                    html_invoice_file.write(invoice_html)

                # Prepare seller picklist pdf
                cur_seller_picklist_html = picklist_template_parts[0] + cur_picklist_record_data
                cur_seller_picklist_html = cur_seller_picklist_html.replace("SELLER_NAME",
                                                                            seller_agg[seller_email][
                                                                                'seller'].first_name + " " +
                                                                            seller_agg[seller_email][
                                                                                'seller'].last_name).replace(
                    "SELLER_EMAIL", seller_email).replace("SELLER_COMPANY",
                                                          seller_agg[seller_email]['seller'].company.company_name)
                cur_seller_picklist_file_name = "picklist_" + order_id + "__" + \
                                                order.customer.name.replace(
                                                    " ", "") + "__" + str(time.time()) + ".pdf"
                cur_seller_full_picklist_save_path = os.path.join(
                    settings.MEDIA_ROOT, 'picklists', cur_seller_picklist_file_name)
                order.invoice_filepath = cur_seller_full_picklist_save_path
                order.save()
                HTML(string=cur_seller_picklist_html).write_pdf(cur_seller_full_picklist_save_path)

                ##CHANGE 7 7:28 PM

                #Prepare seller purchase order pdf
                cur_seller_po_html = purchase_order_template_parts[0] + cur_purchaseorder_record_data
                cur_seller_po_html = cur_seller_po_html.replace(
                    "SELLER_NAME", seller_agg[seller_email]['seller'].first_name + " " + seller_agg[seller_email][
                        'seller'].last_name).replace("SELLER_EMAIL", seller_email)
                cur_seller_po_html = cur_seller_po_html.replace("GRAND_TOTAL", str(order_total)).replace(
                    "SELLER_COMPANY", seller_agg[seller_email]['seller'].company.company_name)
                cur_seller_po_file_name = "po_" + order_id + "__" + \
                                          order.customer.name.replace(
                                              " ", "") + "__" + str(time.time()) + ".pdf"
                cur_seller_po_full_file_save_path = os.path.join(
                    settings.MEDIA_ROOT, 'purchase_orders', cur_seller_po_file_name)
                HTML(string=cur_seller_po_html).write_pdf(cur_seller_po_full_file_save_path)
                # pdfkit.from_string(cur_seller_po_html,
                #                    cur_seller_po_full_file_save_path, verbose=True)
                # Save invoice for buyer email

                ##
                buyer_purchase_orders.append(cur_seller_po_full_file_save_path)

                cur_seller_msg = f"""
                Dear {seller_agg[seller_email]['seller'].first_name} {seller_agg[seller_email]['seller'].last_name},
                
                You just sold products on GustoMarket! Attached to this email, you will find an invoice for the transaction.
                
                Best,
                
                The GustoMarket Team
                """
                seller_notif, _ = Notification.objects.get_or_create(user=seller_agg[seller_email]['seller'].user,
                                                                     message=cur_seller_msg)

                send_notification_email(seller_email, f"You just Sold Product on GustoMarket!", cur_seller_msg, [
                    cur_seller_po_full_file_save_path, cur_seller_full_picklist_save_path])
            # Handle buyer notification/email
            buyer_msg = f"""
            Dear {order.customer.name},

            Thank you for your recent order with GustoMarket. The grand total of your order was ${order.grand_total}.

            Attached to this email, you will find your purchase invoices, separated by supplier.

            Best,

            The GustoMarket Team
            """
            buyer_notif, _ = Notification.objects.get_or_create(
                user=buyer, message=buyer_msg)
            # send_notification_email(buyer_email, "Thank you for your Purchase with GustoMarket!", buyer_msg,
            #                         buyer_invoices)  # Email buyer
            send_notification_email(buyer_email, "Thank you for your Purchase with GustoMarket!", buyer_msg,
                                    buyer_purchase_orders)

            print(f'Invoice filepath saved: {order.invoice_filepath}')
            print("Sent buyer email to ", buyer_email)
            del request.session['order_id']

            # Display a confirmation message
            messages.success(
                request, 'Payment successful. Thank you for your order!')

            return render(request, 'payment_success.html', {'order': order})
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
    else:
        messages.error(request, 'Invalid order ID.')

    # Redirect to the home page
    return redirect('/')


def get_safe_sku_unit_external(v):
    if v is None:
        return "Standard (Unspecified)"
    else:
        if v.unit_option is None:
            return "Standard (Unspecified)"
        else:
            return v.unit_option


def payment_cancel(request):
    """
    return to the cart page for a cancel payment.
    """
    order_id = request.session.get('order_id')

    if order_id:
        try:
            order = Order.objects.get(orderID=order_id)
            order.payment_status = 'cancell'
            order.save()

            # Clear the session variable
            del request.session['order_id']

            # Display a confirmation message
            messages.success(
                request, 'Payment cancel!')

            return redirect('cart')

        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
    else:
        messages.error(request, 'Invalid order ID.')

    # Redirect to the home page
    return redirect('/')


def get_picklist_data(request, order_id):
    order = Order.objects.get(orderID=order_id)
    eastern_time = datetime.now(pytz.timezone('US/Eastern'))

    with open(r"Services/templates/picklist_template.html") as p:
        picklist_html = p.read()

    picklist_html = picklist_html.replace("BUYER_NAME", order.customer.name).replace("ORDER_ID", order_id).replace(
        "ORDER_SEC", order.order_date.strftime("%y%m") + str(order.id)) \
        .replace("BUYER_EMAIL", order.customer.email).replace(
        "BUYER_ADDR_LINE1",
        order.customer.address.address_lane_1 if order.customer.address else "") \
        .replace("BUYER_CITY", order.customer.address.city if order.customer.address else "") \
        .replace("BUYER_STATE", order.customer.address.state.state_name if order.customer.address else "") \
        .replace("BUYER_ZIP", order.customer.address.zip_code if order.customer.address else "")
    picklist_html = picklist_html.replace(
        "CURRENT_DATE", eastern_time.strftime("%B %d, %Y %I:%M %p"))
    picklist_template_parts = picklist_html.split("<!--DATA_GOES_HERE-->")

    seller_agg = {}
    for prod in order.products.all():
        cur_seller_email = prod.supplier.email
        if cur_seller_email not in seller_agg.keys():
            seller_agg[cur_seller_email] = {
                'seller': prod.supplier, 'products': []}
        seller_agg[cur_seller_email]['products'].append(prod)

    def get_safe_sku_packaged(v):
        if v is None:
            return "Standard (Unspecified)"
        else:
            if v.selling_option is None:
                return "Standard (Unspecified)"
            else:
                return v.selling_option

    # Iterate through the aggregated sellers (two loops instead of one for readability.
    for seller_email in seller_agg.keys():
        products_sold = {}
        for p in seller_agg[seller_email]['products']:
            if p.product_title not in products_sold.keys():
                products_sold[p.product_title] = 1
            else:
                products_sold[p.product_title] += 1

    cur_picklist_record_data = ""
    cur_added_items = set()
    order_total = 0
    order_items = OrderItem.objects.filter(
        order__orderID=order_id, product__supplier=seller_agg[seller_email]['seller'])
    for order_item in order_items.all():
        if order_item.product.product_title in cur_added_items:
            continue
        order_total += order_item.total_price * order_item.quantity

        cur_picklist_record_data += f"""
                       
                        
                        
                        <tr>
                            <td style="margin-right:5px; font-size:14px;">{order_item.product.product_title}<br>{order_item.product.description}</td>
                            <td>{order_item.quantity}</td>
                            <td>{get_safe_sku_packaged(order_item.product.product_packaging.sku_sold)}</td>
                            <td>
                                <label class="checkbox-label" style="margin-left:42px;">
                                <input type="checkbox" class="custom-checkbox">
                                <span class="checkmark"></span>
                                </label>
                            </td>
                            <td>
                                <label class="checkbox-label"style="margin-left:42px;">
                                <input type="checkbox" class="custom-checkbox">
                                <span class="checkmark"></span>
                                </label>
                            </td>
                            <td>
                                <label class="checkbox-label"style="margin-left:28px;">
                                <input type="checkbox" class="custom-checkbox">
                                <span class="checkmark"></span>
                                </label>
                            </td>

			            </tr>                  


                        """

    # Prepare seller picklist pdf
    cur_seller_picklist_html = picklist_template_parts[0] + cur_picklist_record_data  #picklist_template_parts[1]
    cur_seller_picklist_html = cur_seller_picklist_html.replace("SELLER_NAME",
                                                                seller_agg[seller_email]['seller'].first_name + " " +
                                                                seller_agg[seller_email]['seller'].last_name).replace(
        "SELLER_EMAIL", seller_email).replace("SELLER_COMPANY", seller_agg[seller_email]['seller'].company.company_name)
    cur_seller_picklist_file_name = "picklist_" + order_id + "__" + \
                                    order.customer.name.replace(
                                        " ", "") + "__" + str(time.time()) + ".pdf"
    cur_seller_full_picklist_save_path = os.path.join(
        settings.MEDIA_ROOT, 'picklists', cur_seller_picklist_file_name)
    order.invoice_filepath = cur_seller_full_picklist_save_path
    order.save()
    HTML(string=cur_seller_picklist_html).write_pdf(cur_seller_full_picklist_save_path)
    pdf_url = f"{settings.MEDIA_URL}picklists/{cur_seller_picklist_file_name}"

    return render(request, 'show_pdf.html', {'pdf_url': pdf_url})


def get_invoice_data(request, order_id):
    # Fetch the order based on the order ID
    order = Order.objects.get(orderID=order_id)
    eastern_time = datetime.now(pytz.timezone('US/Eastern'))

    # Load the HTML invoice template
    with open(r"Services/templates/invoice_template.html") as f:
        invoice_html = f.read()

    # Replace placeholders with order and customer details
    invoice_html = invoice_html.replace("BUYER_NAME", order.customer.name) \
        .replace("ORDER_ID", order_id) \
        .replace("CLIENT_NUMBER", order.customer.stripe_customer_id) \
        .replace("BUYER_EMAIL", order.customer.email) \
        .replace("BUYER_ADDR_LINE1", order.customer.address.address_lane_1 if order.customer.address else "") \
        .replace("BUYER_CITY", order.customer.address.city if order.customer.address else "") \
        .replace("BUYER_STATE", order.customer.address.state.state_name if order.customer.address else "") \
        .replace("BUYER_ZIP", order.customer.address.zip_code if order.customer.address else "") \
        .replace("CURRENT_DATE", eastern_time.strftime("%B %d, %Y %I:%M %p")) \
        .replace("DUE_DATE", "Aug 15, 2024, 4:00pm") \
        .replace("PAYMENT_TERMS", str(order.payment))

    # Add seller details
    invoice_html = invoice_html.replace("SELLER_COMPANY", order.customer.name if order.customer else "") \
        .replace("SELLER_EMAIL", order.customer.email if order.customer else "")

    
    items_html = ""
    grand_total = 0
    for item in OrderItem.objects.filter(order=order):
        # Get transport price, defaulting to 0 if not available
        # product_price = item.product.price_transport.amount if item.product.price_transport.amount else 0
        item_total = item.total_price * item.quantity
        grand_total += item_total  

        # Create a row for each item, handling potential None values
        packaging_unit = item.product.product_packaging.sku_unit if item.product.product_packaging else ""
        items_html += f"""
        <tr class="item">
            <td style="width: 40%; text-align: left;">{item.product.product_title}<p style="font-size: small; color:#606060;">{item.product.description}</p></td> 
            <td class="qt" style="width: 12%; text-align:center;">{item.quantity}</td> 
            <td style="width: 12%; text-align:center;">{item.product.product_packaging.sku_sold}</td>
            
            <td style="width: 12%; text-align:center;">{item.total_price}</td>
           
            <td style="width: 12%; text-align:center;"> {item.product.product_packaging.sku_unit}</td>
            <td style="width: 12%; text-align:center;">{item.quantity*item.total_price:.2f}</td>
        </tr>
        """

    # Replace placeholder for order items
    invoice_html = invoice_html.replace("<!-- DATA_GOES_HERE -->", items_html)

    # Replace grand total placeholder
    invoice_html = invoice_html.replace("GRAND_TOTAL", f"${grand_total:.2f}")

    # Save the generated invoice HTML to a file
    cur_seller_invoice_file_name = "invoice_" + order_id + "__" + \
                                   order.customer.name.replace(" ", "") + "__" + str(time.time()) + ".pdf"
    cur_seller_html_filepath = os.path.join(settings.MEDIA_ROOT, 'invoices', cur_seller_invoice_file_name)
    order.invoice_filepath = cur_seller_html_filepath
    order.save()

    with open(cur_seller_html_filepath, "w") as html_invoice_file:
        html_invoice_file.write(invoice_html)

    # Generate PDF from HTML
    HTML(string=invoice_html).write_pdf(cur_seller_html_filepath)
    pdf_url = f"{settings.MEDIA_URL}invoices/{cur_seller_invoice_file_name}"

    return render(request, 'show_pdf.html', {'pdf_url': pdf_url})


def get_purchase_order(request, order_id):
    order = Order.objects.get(orderID=order_id)
    order_items = OrderItem.objects.filter(order__orderID=order_id)
    eastern_time = datetime.now(pytz.timezone('US/Eastern'))

    grand_total = Decimal('0.0')

    

    cur_purchaseorder_record_data = f"""
    
    <table  style="position: fixed;top:45%; right:0.2%; width: 100%;border-collapse: collapse;">
                <thead style="margin-right: 75px; background-color: white;">
                    <tr class="heading" style="padding:2px; padding-left:130px;padding:5px" >
                        <td class="qt">
                            <p style="font-weight: bold; color:#555;"><strong>Product</strong></p>

                        </td>
                        <td class="qt" style="padding:2px;">
                            <p style="font-weight: bold; color:#555;margin-left:2px"><strong>Quantity</strong></p>
                        </td>
                        <td class="qt" style="padding:2px;">
                            <p style="font-weight: bold; color:#555; "><strong>Unit Sold</strong></p>
                        </td> 
                        <td class="qt" style="text-align: left;" style="padding:2px;">
                            <p style="font-weight: bold; color:#555; "><strong>Unit price</strong></p>
                        </td>
                        <td class="qt" style="padding:2px; ">
                            <p style="font-weight: bold; color:#555;  "><strong>Unit of Pricing</strong></p>
                        </td>
                        <td class="qt" style="text-align: left;"style="padding:2px;">
                            <p style="font-weight: bold; color:#555;"><strong>Sub Total</strong></p>
                        </td>
                    </tr>
                  
                    

                </thead>
          
                """

    for order_item in order_items:
        # product_title = order_item.product.product_title[:15]
        # if len(order_item.product.product_title) > 15:
        #     product_title += "..."
        quantity = Decimal(order_item.quantity)
        unit_price = Decimal(order_item.total_price)
        subtotal =  quantity * unit_price
    
        grand_total += subtotal
        sku_sold = order_item.product.product_packaging.sku_sold if order_item.product.product_packaging else "N/A"
        sku_unit = order_item.product.product_packaging.sku_unit if order_item.product.product_packaging else "N/A"

        cur_purchaseorder_record_data += f"""
            <tr style"position:relative; margin-right: 70px">
               <td class="qt">
                    <p >{order_item.product.product_title}</p>
                    <p style="font-size: small; color:#606060;">{order_item.product.description}</p>
               </td>
                <td class="qt" style="text-align: center;"width: 12%;">
                   <p style="text-align: center;">{order_item.quantity}</p>
                </td>
                <td class="qt" style="text-align: center;"width: 12%;">
                   <p style="text-align: center;">{sku_sold}</p>
                </td>
                <td class="qt" style="text-align: center;"width: 12%; ">
                    <p>{order_item.total_price}</p>
               </td>
                <td class="qt" style="text-align: center;"width: 12%;">
                   <p style="text-align: center; ">{sku_unit}</p>
                </td>

               <td class="qt" style="text-align: center;"width: 12%;">
                    <p>${subtotal:.2f}</p>
               </td>
            </tr>
        """
    cur_purchaseorder_record_data += f"""
        <!-- DATA GOES HERE -->
        </tbody>
        <tfoot>
            <tr>
                <td colspan="5" style="text-align: right; font-weight: bold; padding: 10px; color: #555">
                    <b style="font-size: 18px;">Grand Total: </b>
                </td>
                <td style="text-align: left; font-weight: bold; padding: 10px; color:#555">
                    ${grand_total:.2f}
                </td>
            </tr>
        </tfoot>

    </table>
    <p style="font-size: 18px; text-align: right; font-weight: bold; padding-top: 10px; margin-right: 20px;">
        Grand Total: <span style="color: #000;">${grand_total:.2f}</span>
    </p>
           
    """
    with open(r"Services/templates/purchase_order_template.html") as f:
        purchase_order_html = f.read()

    buyer_address = order.customer.address
    purchase_order_html = purchase_order_html.replace("BUYER_NAME", order.customer.name).replace("ORDER_ID",
                                                                                                 order_id).replace(
        "ORDER_SEC", order.order_date.strftime("%y%m") + str(order.id)) \
        .replace("BUYER_EMAIL", order.customer.email).replace("BUYER_ADDR_LINE1",
                                                              buyer_address.address_lane_1 if buyer_address else "Address not available") \
        .replace("BUYER_CITY", buyer_address.city if buyer_address else "City not available") \
        .replace("BUYER_STATE",
                 buyer_address.state.state_name if buyer_address and buyer_address.state else "State not available") \
        .replace("BUYER_ZIP", buyer_address.zip_code if buyer_address else "ZIP not available") \
        .replace('BUYER_COMPANY_NAME', buyer_address.location if buyer_address else "Company not available") \

    new_date = order.order_date + timedelta(days=5)
    purchase_order_html = purchase_order_html.replace(
        "DELIVERY_DATE", new_date.strftime("%B %d, %Y %I:%M %p"))
    purchase_order_html = purchase_order_html.replace(
        "PAYMENT_TERMS", str(order.payment))

    purchase_order_html = purchase_order_html.replace("CURRENT_DATE", order.order_date.strftime("%B %d, %Y %I:%M %p"))
    purchase_order_template_parts = purchase_order_html.split("<!--DATA_GOES_HERE-->")
    # Ensure to format the grand total as a string with two decimal places
    


    # Seller Aggregation for Invoice Generation
    seller_agg = {}
    for prod in order.products.all():
        cur_seller_email = prod.supplier.email
        if cur_seller_email not in seller_agg.keys():
            seller_agg[cur_seller_email] = {
                'seller': prod.supplier, 'products': []}
        seller_agg[cur_seller_email]['products'].append(prod)

    # Iterate through the aggregated sellers (two loops instead of one for readability.
    for seller_email in seller_agg.keys():
        products_sold = {}
        for p in seller_agg[seller_email]['products']:
            if p.product_title not in products_sold.keys():
                products_sold[p.product_title] = 1
            else:
                products_sold[p.product_title] += 1

        order_total = 0

        cur_seller_po_html = purchase_order_template_parts[0] + cur_purchaseorder_record_data

        cur_seller_po_html = cur_seller_po_html.replace(
            "SELLER_NAME",
            seller_agg[seller_email]['seller'].first_name + " " + seller_agg[seller_email]['seller'].last_name)

        cur_seller_po_html = cur_seller_po_html.replace("GRAND_TOTAL", str(order_total)).replace(
            "SELLER_COMPANY", seller_agg[seller_email]['seller'].company.company_name)
        cur_seller_po_html = cur_seller_po_html.replace("SELLER_PHONE", seller_agg[seller_email]['seller'].phone if seller_agg[seller_email]['seller'].phone else "Not Available")

    cur_seller_po_file_name = "po_" + order_id + "__" + \
                              order.customer.name.replace(
                                  " ", "") + "__" + str(time.time()) + ".pdf"
    cur_seller_po_full_file_save_path = os.path.join(
        settings.MEDIA_ROOT, 'purchase_orders', cur_seller_po_file_name)
    with open(cur_seller_po_full_file_save_path, "w") as html_invoice_file:
        html_invoice_file.write(cur_seller_po_html)

    HTML(string=cur_seller_po_html).write_pdf(cur_seller_po_full_file_save_path)
    pdf_url = f"{settings.MEDIA_URL}purchase_orders/{cur_seller_po_file_name}"

    return render(request, 'show_pdf.html', {'pdf_url': pdf_url, })
