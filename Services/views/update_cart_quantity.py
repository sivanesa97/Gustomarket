"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.http import JsonResponse
from django.db import transaction
from Services.models import Cart
from Services.views.cart_calculation import calculate_cart


def update_cart_quantity(request, cart_item_id):
    """
    View function to update the quantity of a product in the user's cart.
    """
    try:
        cart_item = Cart.objects.filter(
            user=request.user, id=cart_item_id).first()

        # receive the new quantity from the AJAX request
        new_quantity = int(request.POST.get('quantity'))
        supplier_id = int(request.POST.get('supplier_id'))
        product_id = int(request.POST.get('product_id'))
        print("Updating cart quantity: ", new_quantity)
        with transaction.atomic():
            # Update the quantity in the cart item
            cart_item.quantity = new_quantity
            cart_item.save()

            # Recalculate cart details
            cart_items = Cart.objects.filter(user=request.user)
            vendors, grand_total = calculate_cart(cart_items)

            selected_vendor_data = None
            for supplier, data in vendors.items():
                if supplier.id == supplier_id:
                    selected_vendor_data = {
                        'supplier_id': supplier.id,
                        'subtotal': data['subtotal'],
                        'discount': data['discount'],
                        'tax': data['tax'],
                        'delivery_fee': data['delivery_fee'],
                        'total_price': [total_price for _, product, _, total_price
                                        in data['products'] if product.id == product_id],
                        'total': data['total'],
                        'grand_total': grand_total,
                        'cart_item_count': sum(cart_item.quantity for cart_item in cart_items)
                    }
                    break
            return JsonResponse(selected_vendor_data)

    except Exception as error:
        print(f"An error occurred: {str(error)}")
        return JsonResponse({'error': 'An error occurred while updating the cart'})
