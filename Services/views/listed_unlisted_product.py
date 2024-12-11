"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
# from django.core.paginator import Paginator
from Services.models import Supplier, Product


@login_required(login_url='sign_in')
def listed_unlisted_product(request):
    """
    List all the active and drafts products, also can be published and deleted multiple products.
    """
    # Initialize variables
    error_message, supplier, products = [None] * 3
    try:
        # Get the supplier associated with the current user
        supplier = Supplier.objects.get(user=request.user)
        products = Product.objects.filter(
            supplier__user=request.user, is_active=True)

        # paginator = Paginator(products, 2)

        if request.method == 'POST':
            # Get the list of selected products
            selected_products = request.POST.getlist('selected_products')
            products_to_delete = Product.objects.filter(
                id__in=selected_products, supplier__user=request.user)

            # Handle different actions based on the 'publish_action' POST parameter
            publish_action = request.POST.get('publish_action')
            if publish_action == 'delete':
                # Make selected products in active.
                for product in products_to_delete:
                    product.is_active = False
                    product.save()

            elif publish_action == 'listed':
                # Mark selected products as not drafts and save them
                for product in products_to_delete:
                    product.is_draft = False
                    product.save()

            else:
                # Mark selected products as drafts and save them
                for product in products_to_delete:
                    product.is_draft = True
                    product.save()

            return HttpResponseRedirect(request.path_info)

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
