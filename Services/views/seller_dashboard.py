"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.conf import settings
from datetime import timedelta
from decimal import Decimal
from weasyprint import HTML
from Services.models import Supplier, Customer, Tooltip, TooltipData
from Services.models import SkuSold
from Services.models.product_order import OrderItem, Order
from Services.models.order_delivery import ProductDeliveryIssue
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from Services.models.product_dimension_weight import ProductWeight
import logging
import os
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


# ****************** seller dashboard functionality start here ***************


@login_required(login_url='sign_in')
def seller_dashboard(request):
    """
    Render seller dashboard.
    """
    try:
        supplier = Supplier.objects.get(user=request.user)
        customer = Customer.objects.filter(user=request.user).first()
        print(customer)
        print(f'Supplier {supplier}')
        time_period = request.GET.get('time_period')

        if time_period == 'one_day':
            sold_items = OrderItem.objects.filter(
                product__supplier=supplier, order__order_date__gte=timezone.now() - timedelta(days=1))
            purchased_items = OrderItem.objects.filter(
                order__customer=customer, order__order_date__gte=timezone.now() - timedelta(days=1))
        elif time_period == 'two_day':
            sold_items = OrderItem.objects.filter(
                product__supplier=supplier, order__order_date__gte=timezone.now() - timedelta(days=2))
            purchased_items = OrderItem.objects.filter(
                order__customer=customer, order__order_date__gte=timezone.now() - timedelta(days=2))
        else:
            sold_items = OrderItem.objects.filter(product__supplier=supplier)
            purchased_items = OrderItem.objects.filter(
                order__customer=customer)

        if not customer:
            purchased_items = None

        tooltip = Tooltip.objects.filter(
            page_name__icontains='dashboard').first()
        tooltip_data = TooltipData.objects.filter(page_name=tooltip)

        total_value = sum(order_item.total_price for order_item in sold_items)
        total_fee = sum(order_item.total_fee for order_item in sold_items)

        sold_dict, sold_combined, sold_units, customer_names = aggregate_sold(
            sold_items)
        purchased_dict, purchased_combined, purchased_units = aggregate_purchased(
            purchased_items)

        unit_choices = SkuSold.objects.all()

        if request.method == 'POST':

            '''seller's side'''
            item_id = request.POST.get(
                'soldOrderedItemId')  # obtain orderID corresponding to modal
            print(item_id)
            if request.POST.get("datePicker") and item_id:
                order_items_list = sold_dict[item_id][2]
                for item in order_items_list:
                    orderitems = (OrderItem.objects.filter(
                        product=item[0].product, order__orderID=item_id))
                    for orderitem in orderitems:
                            orderitem.requested_date = request.POST.get("datePicker")
                            orderitem.save()
            if item_id is not None:
                sold_publish_action = request.POST.get(
                    'sold_ordered_publish_action_' + item_id)
                order_items_list = sold_dict[item_id][2]
                # to transfer products from ordered to in-transit
                if sold_publish_action == 'change_to_in_transit':
                    for item in order_items_list:
                        orderitems = (OrderItem.objects.filter(
                            product=item[0].product, order__orderID=item_id))
                        for orderitem in orderitems:
                            orderitem.order_status = 'in_transit'
                            orderitem.save()

                # to edit products in sold ordered
                elif sold_publish_action == 'edit_products':
                    # to edit quantity of products
                    quantities = request.POST.getlist('sold-item-qty-' + item_id)
                    count = 0
                    try:
                        for item in order_items_list:
                            old_quantity = OrderItem.objects.filter(
                                product=item[0].product, order__orderID=item_id).count()
                            new_quantity = int(quantities[count])

                            if new_quantity < old_quantity:  # delete order item instances
                                while new_quantity != old_quantity:
                                    orderitems = OrderItem.objects.filter(
                                        product=item[0].product, order__orderID=item_id)
                                    delete_item(orderitems)
                                    old_quantity -= 1
                            elif new_quantity > old_quantity:  # add order item instances
                                while new_quantity != old_quantity:
                                    create_new_item(item[0])
                                    old_quantity += 1
                            orderitems = OrderItem.objects.filter(
                                product=item[0].product, order__orderID=item_id)
                            print(len(orderitems))
                            for orderitem in orderitems:
                                orderitem.quantity = new_quantity
                                orderitem.save()
                            count += 1

                    except Exception as error:
                        error_message = f"An unexpected error occurred while changing item quantities: {error}"

                    # to edit unit prices of products
                    prices = request.POST.getlist('price-' + item_id)
                    print(prices)
                    count = 0
                    for item in order_items_list:
                        orderitems = (OrderItem.objects.filter(
                            product=item[0].product, order__orderID=item_id))
                        for orderitem in orderitems:
                            orderitem.total_price = Decimal(prices[count])
                            orderitem.save()
                        count += 1

                    # to add/edit weights of products
                    weight_values = request.POST.getlist(
                        'weight-value-' + item_id)
                    count = 0
                    print(weight_values)
                    for item in order_items_list:
                        orderitems = (OrderItem.objects.filter(
                            product=item[0].product, order__orderID=item_id))
                        for orderitem in orderitems:
                            orderitem.skusold_weight = Decimal(
                                weight_values[count])
                            orderitem.save()
                        count += 1

                    # to edit picked attribute of products
                    picked_product_ids = request.POST.getlist(
                        'picked_products')
                    picked_items = []
                    for product_id in picked_product_ids:
                        picked_items += OrderItem.objects.filter(
                            product__id=product_id, order__orderID=item_id)
                    for item in picked_items:
                        item.picked = 'yes'
                        item.save()

            # update delivery issue with order & product
            in_transit_id = request.POST.get('soldInTransitItemId')
            if in_transit_id:
                order_id = Order.objects.filter(orderID=in_transit_id).first()
                data = {
                    "user": request.user,
                    "order": order_id,
                    "perfect_delivery": True if request.POST.get('perfect_delivery') else False,
                    "damage_check": True if request.POST.get('damage_check') else False,
                    "missing_product": True if request.POST.get('missing_product') else False,
                    "overall_service": True if request.POST.get('overall_service') else False,
                    "damage_other_category": request.POST.get('damage_other_category'),
                    "other_note": request.POST.get('other_note'),
                    "issue_files": request.FILES.get('issue_files'),  # Use FILES for file fields
                    "content": request.POST.get('content'),
                }

                # Specify a unique field (or combination of fields) to match for updating or creating
                ProductDeliveryIssue.objects.update_or_create(
                    defaults=data  # Fields to update/create with
                )

            in_delivered_id = request.POST.get('soldInDeliveredItemId')
            if in_delivered_id:
                order = Order.objects.filter(orderID=in_delivered_id).first()
                payment_status = request.POST.get("order_paid")
                if order:
                    order.is_paid = True if payment_status else False
                    order.save()


            '''buyer's side'''
            item_id = request.POST.get(
                'purchasedOrderedItemId')  # obtain orderID corresponding to modal
            if item_id is not None:
                # obtain orderID and supplierID corresponding to modal
                order_id = item_id.split('.')[0]
                supplier_id = int(item_id.split('.')[1])
                order_supplier = Supplier.objects.get(id=supplier_id)
                purchased_publish_action = request.POST.get(
                    'purchased_ordered_publish_action_' + item_id)
                purchased_items_list = purchased_dict[(
                    order_id, order_supplier)][2]
                # edit products in ordered purchased section
                if purchased_publish_action == 'edit_products':
                    quantities = request.POST.getlist(
                        'purchased-item-qty-' + item_id)
                    count = 0
                    try:
                        print("ORDER_ID", order_id)
                        for item in purchased_items_list:
                            old_quantity = OrderItem.objects.filter(
                                product=item[0].product, order__orderID=order_id).count()
                            new_quantity = int(quantities[count])

                            if new_quantity < old_quantity:  # delete order item instances
                                while new_quantity != old_quantity:
                                    orderitems = OrderItem.objects.filter(
                                        product=item[0].product, order__orderID=order_id)
                                    delete_item(orderitems)
                                    old_quantity -= 1
                            elif new_quantity > old_quantity:  # add order item instances
                                while new_quantity != old_quantity:
                                    create_new_item(item[0])
                                    old_quantity += 1
                            orderitems = OrderItem.objects.filter(
                                product=item[0].product, order__orderID=order_id)
                            print(len(orderitems))
                            for orderitem in orderitems:
                                orderitem.quantity = new_quantity
                                orderitem.save()
                            count += 1
                    except Exception as error:
                        error_message = f"An unexpected error occurred while changing item quantities: {error}"

            item_id = request.POST.get(
                'purchasedInTransitItemId')  # obtain orderID corresponding to modal
            if item_id is not None:
                # obtain orderID and supplierID corresponding to modal
                order_id = item_id.split('.')[0]
                supplier_id = int(item_id.split('.')[1])
                order_supplier = Supplier.objects.get(id=supplier_id)
                purchased_publish_action = request.POST.get(
                    'purchased_in_transit_publish_action_' + item_id)
                purchased_items_list = purchased_dict[(
                    order_id, order_supplier)][2]

                # transfer in transit items to delivered tab
                if purchased_publish_action == 'change_to_delivered':
                    for item in purchased_items_list:
                        orderitems = (OrderItem.objects.filter(
                            product=item[0].product, order__orderID=order_id))
                        for orderitem in orderitems:
                            orderitem.order_status = 'delivered'
                            orderitem.save()
                print(order_id)

            return HttpResponseRedirect(request.path_info)

        context = {
            'purchased_combined': purchased_combined,
            'purchased_items': purchased_items,
            'purchased_units': purchased_units,
            'sold_combined': sold_combined,
            'sold_items': sold_items,
            'sold_units': sold_units,
            'customer_names': customer_names,
            'order_count': len(sold_combined),
            'formatted_total_value': format_large_number(total_value),
            'total_fee': format_large_number(total_fee),
            'tooltip_data': tooltip_data,
            'unit_choices': unit_choices,
        }

        return render(request, 'dashboard-seller.html', context)

    except Supplier.DoesNotExist:
        error_message = 'Supplier not found'

    except Exception as error:
        # Handle unexpected errors and provide an error message
        error_message = f"An unexpected error occurred: {error}"

    return render(request, 'dashboard-seller.html', {'error_message': error_message})


# ****************** seller dashboard functionality end here ***************


## ***************** function to build invoice *****************************
def populate_invoice_data(order, order_items, invoice_html_content):
    invoice_template_parts = invoice_html_content.split("DATA_GOES_HERE")

    print('Strting to create invoice...')

    # Iterate through the aggregated sellers (two loops instead of one for readability.
    cur_added_items = set()
    cur_invoice_record_data = ""
    order_total = 0

    for order_item in order_items.all():
        if order_item.product.product_title in cur_added_items:
            continue
        order_total += order_item.total_price * order_item.quantity

        cur_invoice_record_data += f"""
            <tr class="item">
                <td>{order_item.product.product_title}<br><small>{order_item.product.description}</small></td>
                
                <td class='qt'>{order_item.quantity} {get_safe_sku_unit_external(order_item.product.product_packaging.sku_unit)}</td>
                
                <td>${order_item.total_price}</td>
                
                <td>${order_item.total_price * order_item.quantity}</td> 
            </tr>
        """

        cur_added_items.add(order_item.product.product_title)

    print('Order data successfully added')

    cur_seller_invoice_html = invoice_template_parts[0] + \
                              cur_invoice_record_data + \
                              invoice_template_parts[1]
    cur_seller_invoice_html = cur_seller_invoice_html.replace(
        "SELLER_COMPANY", str(order_item.product.supplier.company)).replace(
        "SELLER_EMAIL", str(order_item.product.supplier.email)).replace(
        "GRAND_TOTAL", str(order_total)
    )

    print('Seller information populated')
    cur_seller_invoice_file_name = "invoice_" + order.orderID + "__" + \
                                   order.customer.name.replace(
                                       " ", "") + "__" + str(time.time()) + ".pdf"
    cur_seller_full_file_save_path = os.path.join(
        settings.MEDIA_ROOT, 'invoices', cur_seller_invoice_file_name)
    order.invoice_filepath = cur_seller_full_file_save_path
    HTML(string=cur_seller_invoice_html).write_pdf(cur_seller_full_file_save_path)

    print('pdf generated using weasyprint')
    return cur_seller_full_file_save_path


## ***************** function to build invoice ends here*****************************

# ****************** format large number functionality start here ***************
def format_large_number(value):
    """
    Format a large number in terms of thousands, millions, and billions for US format.
    """
    if value >= 1_000_000_000:
        return f'{round(value / 1_000_000_000, 2)}B'
    elif value >= 1_000_000:
        return f'{round(value / 1_000_000, 2)}M'
    elif value >= 1_000:
        return f'{round(value / 1_000, 2)}K'
    else:
        return str(value)


# ****************** format large number functionality end here ***************

# ****************** aggregation of products start here ***************


def aggregate_sold(sold_items):
    sold_temp = {}
    sold_product_temp = {}
    sold_units = {}
    customer_names = {}

    '''Creates a list of sublists length 4 [sample item of an orderID, 
    number of items in an order ID, list of products in that orderID, order price]. All items 
    that appear are those sold by the current user. Aggregated by orderID and supplier.
    Also returns dictionary of unique product quantity per orderID and company names of customers. '''
    if sold_items is not None:
        for item in sold_items:
            # item.order_status = 'pending'
            # item.save()
            if item.order.orderID not in sold_temp:
                sold_product_temp[(item.order.orderID, item.product)] = [
                    item, item.quantity]
                sold_temp[item.order.orderID] = [
                    item, 1, [sold_product_temp[(item.order.orderID, item.product)]], item.total_price]
                # sold_total_quantity[item.order.orderID] = 1
                customer_names[item.order.orderID] = Supplier.objects.get(
                    user=item.order.customer.user).company
            else:
                sold_temp[item.order.orderID][3] += item.total_price
                sold_temp[item.order.orderID][1] += 1
                # sold_total_quantity[item.order.orderID] += 1
                if (item.order.orderID, item.product) not in sold_product_temp:
                    sold_product_temp[(item.order.orderID, item.product)] = [
                        item, item.quantity]
                    sold_temp[item.order.orderID][2].append(
                        sold_product_temp[(item.order.orderID, item.product)])

    sold_combined = list(sold_temp.values()) if sold_temp else []

    for item in sold_combined:
        sold_units[item[0]] = len(item[2])

    return sold_temp, sold_combined, sold_units, customer_names  # sold_total_quantity


def aggregate_purchased(purchased_items):
    purchased_temp = {}
    purchased_product_temp = {}
    purchased_units = {}

    '''Creates a list of sublists of length 4 [sample item of an orderID, 
        number of items in an order ID, list of products in that orderID, order price]. All items that 
        appear are those purchased by the current user. Each sublist is for a different 
        supplier/order ID. Aggregated by orderID and supplier. Also returns dictionary of unique 
        product quantity per orderID.'''
    if purchased_items is not None:
        for item in purchased_items:
            if (item.order.orderID, item.product.supplier) not in purchased_temp:
                purchased_product_temp[(item.order.orderID, item.product)] = [
                    item, item.quantity]
                purchased_temp[(item.order.orderID, item.product.supplier)] = [
                    item, 1, [purchased_product_temp[(item.order.orderID, item.product)]], item.total_price]
            else:
                purchased_temp[(
                    item.order.orderID, item.product.supplier)][3] += item.total_price
                purchased_temp[(item.order.orderID,
                                item.product.supplier)][1] += 1
                if (item.order.orderID, item.product) not in purchased_product_temp:
                    purchased_product_temp[(item.order.orderID, item.product)] = [
                        item, item.quantity]
                    purchased_temp[(item.order.orderID, item.product.supplier)][2].append(
                        purchased_product_temp[(item.order.orderID, item.product)])

    purchased_combined = list(
        purchased_temp.values()) if purchased_temp else []

    for item in purchased_combined:
        purchased_units[item[0]] = len(item[2])

    return purchased_temp, purchased_combined, purchased_units


# ****************** aggregation of products ends here ***************

# ****************** create new order items starts here ***************


def create_new_item(item):
    OrderItem.objects.create(
        order=item.order,
        product=item.product,
        order_status=item.order_status,
        picked=item.picked,
        quantity=item.quantity,
        subtotal=item.subtotal,
        discount=item.discount,
        tax=item.tax,
        total_fee=item.total_fee,
        total_price=item.total_price,
        total_weight=item.total_weight,
        skusold_weight=item.skusold_weight,
        tracking_number=item.tracking_number,
        shipping_date=item.shipping_date,
        estimated_delivery_date=item.estimated_delivery_date,
        notes=item.notes)


def delete_item(queryset):
    delete = queryset.first()
    delete.delete()


#TODO creating a variable in the form of a JSON block?
# Or inserting variables individually?
def create_new_change(item):
    OrderChange.objects.create(
        order=item['order'],
        product=item['product'],
        change_type=item['change_type'],
        old_change=item['old_detail'],
        new_detail=item['new_detail'],
        date_of_change=item['datetime'],
    )


def create_new_change(orderIn, prod, change_type, old, new, datetime):
    OrderChange.objects.create(
        order=orderIn,
        product=prod,
        change_type=change_type,
        old_change=old,
        new_change=new,
        datetime=datetime
    )

@csrf_exempt
def move_to_ordered(request):
    order_id = request.GET.get('order_id')
    if order_id:
        OrderItem.objects.filter(order__orderID=order_id).update(
         order_status="pending"   
        )
    return ""
def add_order_item_note(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    if request.method == 'POST':
        notes = request.POST.get('content', '')
        attachment = request.FILES.get('attachment')

        if attachment:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'pdf', 'docx']
            ext = os.path.splitext(attachment.name)[1][1:].lower()
            if ext not in allowed_extensions:
                raise ValidationError(f"Unsupported file extension. Allowed types: {', '.join(allowed_extensions)}")

        if notes or attachment:
            order_item.notes = notes
            if attachment:
                order_item.attachment = attachment
            order_item.save()

        return redirect('dashboard') 
    return render(request, 'dashboard-seller.html', {'order_item': order_item})
