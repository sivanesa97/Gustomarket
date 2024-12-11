"""
Importing models is used for creating a database model.
"""
from django.db import models
from .changelog_models import ChangeLog


# """"""""""" Order model start here ****************"
class Order(models.Model):
    """
    A class representing an order of a Product.
    Attributes:
    """
    PAYMENT_STATUS = (
        ('success', 'Success'),
        ('cancell', 'Cancell'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    customer = models.ForeignKey(
        'Services.Customer', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        "Services.Payment", on_delete=models.SET_NULL, blank=True, null=True)
    products = models.ManyToManyField(
        'Services.Product')  # Unique order identifier
    orderID = models.CharField(max_length=255, unique=True)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    is_gift = models.BooleanField(default=False)
    gift_message = models.TextField(blank=True, null=True)
    invoice_filepath = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order {self.orderID} by {self.customer} on {self.order_date}"


# """"""""""" Order model end here ****************"


# """"""""""" Order item model start here ****************"
class OrderItem(models.Model):
    """
    A class representing an order item of an order.
    Attributes:
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    PICKED_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        'Services.Product', on_delete=models.SET_NULL, blank=True, null=True)
    order_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    picked = models.CharField(
        max_length=20, choices=PICKED_CHOICES, default='no')
    quantity = models.PositiveIntegerField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_weight = models.ForeignKey(
        'Services.ProductWeight', on_delete=models.SET_NULL, blank=True, null=True)
    skusold_weight = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    tracking_number = models.CharField(max_length=30, blank=True, null=True)
    shipping_date = models.DateField(blank=True, null=True)
    estimated_delivery_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    requested_date = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return f"Order {self.order}"

    def order_changes(self):
        order_id = self.order.pk
        change_data = ChangeLog.objects.filter(model_name='Order', instance_id=order_id)
        if change_data:
            return change_data
        return None


# """"""""""" Order item model end here ****************"


#"""""""""""" Order change model begins here """"""""""""

class OrderChange(models.Model):
    """
    A class representing the changes made to the order
    on the seller side

    pass
    Attributes:
    """
    # CHANGE_CHOICES = (
    #     ('none', "None"),
    #     ('quantity', 'Quantity'),
    #     ('date', "Date"),
    #     ('weight', "Weight"),
    #     ('product_removed', "Product Removed"),
    #     ('product_added', 'Product Added'),
    #     ('price', "Price"),
    # )
    #
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # product = models.ForeignKey(
    #     'Services.Product', on_delete=models.SET_NULL, blank=True, null=True)
    # change_type = models.CharField(choices=CHANGE_CHOICES, default='none')
    # old_change = models.CharField(max_length=30, blank=True, null=True)
    # new_change = models.CharField(max_length=30, blank=True, null=True)
    # date_of_change = models.DateField(blank=True, null=True)
    #
    # def __str__(self):
    #     return f"Order change"

#"""""""""""" Order change model ends here """"""""""""""
