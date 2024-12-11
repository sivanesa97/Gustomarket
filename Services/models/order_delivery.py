from django.db import models
from Services.models.product_order import Order
from django.contrib.auth.models import User


class ProductDeliveryIssue(models.Model):
    """
    A class representing an order delivery-related issue.

    Attributes:
        order (ForeignKey): Reference to the Order model, nullable and deletable.
        perfect_delivery (BooleanField): Indicates whether the delivery was perfect.
        damage_check (BooleanField): Indicates if there was any damage in the product.
        missing_product (BooleanField): Indicates if any products were missing.
        overall_service (BooleanField): Indicates overall service quality.
        damage_other_category (CharField): Additional details about other types of damage.
        other_note (TextField): Extra notes for any other issues, with a max length of 2000 characters.
        issue_files (FileField): Optional file upload related to the issue.
        content (TextField): Additional content or description of the issue.
        user (ForeignKey): Reference to the User model, nullable and deletable, allowing multiple issues per user.
    """

    order = models.ForeignKey(Order, related_name="product_delivery_issue_order", on_delete=models.CASCADE,
                              null=False, blank=False)
    perfect_delivery = models.BooleanField(default=False)
    damage_check = models.BooleanField(default=False)
    missing_product = models.BooleanField(default=False)
    overall_service = models.BooleanField(default=False)
    damage_other_category = models.CharField(max_length=225, null=True, blank=True)
    other_note = models.TextField(null=True, blank=True, max_length=2000)
    issue_files = models.FileField(null=True, blank=True, upload_to="product_delivery_issues")
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                             related_name="product_delivery_issues")

    def __str__(self):
        return self.order.orderID if self.order else None
