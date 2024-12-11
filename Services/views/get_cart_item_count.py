"""
The modules have imported for different purpose mentioned as below:
JsonResponse : for JsonDta.
"""
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from Services.models import Cart


def get_cart_item_count(request):
    """
    Get total item in the cart using AJAX request.
    """
    try:
        # cart_item_count = Cart.objects.filter(user=request.user).count()
        cart_items = Cart.objects.filter(user=request.user)
        cart_item_count = sum(cart_item.quantity for cart_item in cart_items)
        return JsonResponse({'cart_item_count': cart_item_count})

    except ObjectDoesNotExist:
        error_message = 'Item not found'
        status = 404

    except Exception as error:
        error_message = f'An unexpected error occurred: {error}'
        status = 500

    return JsonResponse({'error_message': error_message}, status=status)
