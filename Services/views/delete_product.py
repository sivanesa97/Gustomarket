"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from Services.models import Product, Supplier


@login_required(login_url='sign_in')
def product_delete(request, pk=None):
    """
    Delete a product with a unique ID.
    """
    # Initialize variables
    error_message, supplier, products = [None] * 3

    try:
        # Get the supplier associated with the current user
        supplier = Supplier.objects.get(user=request.user)
        products = Product.objects.filter(
            supplier__user=request.user, is_draft=True)

        # Check if the product exists before attempting to delete it
        product = Product.objects.filter(id=pk, supplier=supplier).first()
        if product:
            # Make selected product in active.
            product.is_active = False
            product.save()

            return redirect('listed_unlisted_product')

    except ObjectDoesNotExist as error:
        error_message = str(error)

    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"

    context = {
        'supplier': supplier,
        'products': products,
        'error_message': error_message,
    }
    return render(request, 'listed_unlisted_product.html', context)
