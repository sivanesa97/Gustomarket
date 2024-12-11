"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from Services.models import Cart


# @login_required(login_url='sign_in')
def delete_cart_item(request, pk):
    """
    Delete a product with a unique ID in the cart.
    """
    error_message = None
    try:
        # Check if the item exists before attempting to delete it
        cart_item = Cart.objects.filter(id=pk, user=request.user).first()
        if cart_item:
            cart_item.delete()
            return redirect('cart')

    except ObjectDoesNotExist as error:
        error_message = str(error)

    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"

    return render(request, 'listed_unlisted_product.html', {'error_message': error_message})
