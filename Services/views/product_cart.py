"""
The modules have imported for different purposes mentioned as below:
render : to render an HTML template.
login_required : checking if a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from Services.models import Cart, Product, OrderItem, Address
from Services.views.cart_calculation import calculate_cart
from django.utils.html import strip_tags

@login_required(login_url='sign_in')
def cart(request):
    """
    View for rendering the supplier cart.
    """
    error_message = None
    try:
        stripe_publishable_key = settings.STRIPE_PUBLIC_KEY

        with transaction.atomic():
            cart_items = Cart.objects.filter(user=request.user)

            # Calculate cart details
            vendors, grand_total = calculate_cart(cart_items)

            context = {
                'cart_items': cart_items,
                'vendors': vendors,
                'product_count': len(cart_items),
                'grand_total': grand_total,
                'stripe_publishable_key': stripe_publishable_key,
                'error_message': error_message  # Pass any error message to the context if it exists
            }

            return render(request, 'cart.html', context)

    except ObjectDoesNotExist as error:
        error_message = str(error)

    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"

    # Always return a response even in case of an error
    return render(request, 'cart.html', {'error_message': error_message or "An unknown error occurred."})

def product(request):
    """
    View for rendering a specific product.
    """
    error_message = None
    try:
        product = Product.objects.first()  # Get the first product; adjust as needed
        if product:
            product.description = strip_tags(product.description)
            return render(request, 'cart.html', {'product': product})  # Render a specific product template

    except Exception as error:
        error_message = f"Error retrieving product: {str(error)}"

    # Return error response if product retrieval fails
    return render(request, 'error.html', {'error_message': error_message or "An unknown error occurred."})

# @login_required(login_url='sign_in')
# def order_item_view(request):
#     """
#     View for rendering order items.
#     """
#     error_message = None
#     try:
#         order_items = OrderItem.objects.filter(user=request.user)  # Adjust the filter as needed
#         for item in order_items:
#             item.quantity = strip_tags(str(item.quantity))  # Strip tags from quantity if it's a string
#         return render(request, 'cart.html', {'order_items': order_items})  # Render a specific template for order items

#     except Exception as error:
#         error_message = f"Error retrieving order items: {str(error)}"
    
#     # Return error response if order items retrieval fails
#     return render(request, 'error.html', {'error_message': error_message or "An unknown error occurred."})
def cart_view(request):
    order_items = OrderItem.objects.all()  # Retrieve all OrderItem objects
    context = {'order_items': order_items}
    return render(request, 'cart.html', context)
