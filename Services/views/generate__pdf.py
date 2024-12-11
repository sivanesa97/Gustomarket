import time
from django.shortcuts import render, redirect
from django.contrib import messages
from Services.models import Order, Cart, Notification, OrderItem
from decimal import Decimal
from django.conf import settings
import stripe # type: ignore
from Services.views.send_mail import send_notification_email
from datetime import datetime, timedelta
from weasyprint import HTML
import pdfkit
import pytz
import os
import random


def get_picklist_data(request, order_id):
    order = Order.objects.get(orderID=order_id)
    eastern_time = datetime.now(pytz.timezone('US/Eastern'))

    with open(os.path.join(settings.MEDIA_ROOT, "picklist_template.html")) as p:
        picklist_html = p.read()

    picklist_html = picklist_html.replace("BUYER_NAME", order.customer.name).replace("ORDER_ID", order_id) \
        .replace("BUYER_EMAIL", order.customer.email).replace("BUYER_ADDR_LINE1", order.customer.address.address_lane_1) \
        .replace("BUYER_CITY", order.customer.address.city) \
        .replace("BUYER_STATE", order.customer.address.state.state_name) \
        .replace("BUYER_ZIP", order.customer.address.zip_code)
    picklist_html = picklist_html.replace(
        "CURRENT_DATE", eastern_time.strftime("%B %d, %Y %I:%M %p"))
    picklist_template_parts = picklist_html.split("DATA_GOES_HERE")

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
    cur_purchaseorder_record_data = ""  # CHANGE 3 4:15PM
    cur_added_items = set()
    order_total = 0
    order_items = OrderItem.objects.filter(
        order__orderID=order_id, product__supplier=seller_agg[seller_email]['seller'])
    for order_item in order_items.all():
        if order_item.product.product_title in cur_added_items:
            continue
        order_total += order_item.total_price * order_item.quantity

        cur_picklist_record_data = f"""
                            <tr class="item">
                                <td>{order_item.product.product_title}</td>

                                <td>{order_item.quantity}</td>

                                <td>{get_safe_sku_packaged(order_item.product.product_packaging.sku_sold)}</td>
                                <td><div class="square"></div></td>
                                <td><div class="square"></div></td>
                                <td><div class="square"></div></td>
                            </tr>
                        """

    # Prepare seller picklist pdf
    cur_seller_picklist_html = picklist_template_parts[0] + \
                               cur_picklist_record_data + picklist_template_parts[1]
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
    return render(request, 'show_pdf.html',
                  {'pdf_url': cur_seller_full_picklist_save_path, 'MEDIA_URL': settings.MEDIA_URL})


