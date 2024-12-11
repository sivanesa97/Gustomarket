"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
ValidationError: If the new password does not meet validation criteria.
"""
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from Services.models import Cart, Product, Address

logger = logging.getLogger(__name__)


@login_required(login_url='login/')
@transaction.atomic
def add_to_cart(request, product_id):
    """
    Add a product to the user's cart.
    Returns:
    - Redirects to the cart page after adding the product to the cart.
    """
    try:
        product = Product.objects.get(pk=product_id)

        # Check if the product is already in the cart for the user or session
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product)

        # If the item is already in the cart, increase the quantity
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        # cart_item_count = Cart.objects.filter(user=request.user).count()
        cart_items = Cart.objects.filter(user=request.user)
        cart_item_count = sum(cart_item.quantity for cart_item in cart_items)
        return JsonResponse({'success': True,
                             'message': 'Product added to cart',
                             'cart_item_count': cart_item_count})

    except Product.DoesNotExist:
        message = "Product does not exist."
    except Exception as error:
        message = str(error)

    return JsonResponse({'success': False, 'message': message})
