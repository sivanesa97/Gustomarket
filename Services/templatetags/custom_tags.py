"""
The modules have imported for different purpose mentioned as below:
"""
from django.template.defaulttags import register
from django import template
from Services.models.order_delivery import ProductDeliveryIssue
from Services.models.address import Address
# from Service.models.product_order import Order
# from Services.models.changelog_models import ChangeLog


@register.filter
def get_item(dictionary, key):
    """
    get_item
    """
    return dictionary.get(key)


register = template.Library()


@register.simple_tag
def get_issues_by_order(order_id):
    """
    A custom template tag to fetch ProductDeliveryIssue objects by order_id.
    """
    return ProductDeliveryIssue.objects.filter(order__orderID=order_id).first()

@register.simple_tag
def get_location_by_user(user_id):
    address = Address.objects.filter(supplier_id__id=user_id)
    return address



# @register.simple_tag
# def get_order_history(order_id):
#     order = Order.objects.get(pk=order_id)
#     model_name = "Order"
#     get_change_logs = ChangeLog.objects.filter(
#         model_name=model_name,
#         instance_id=order_id,
#     )
#     return get_change_logs
