"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from Services.models import Product


@login_required(login_url='sign_in')
def product_info(request, pk):
    """
    product_info
    """
    try:
        # Get selected product instance.
        product = Product.objects.get(id=pk)

        # Search for related products based on title, category
        # and subcategory of the selected product.
        products = Product.objects.filter(
            Q(product_title=product.product_title) |
            Q(product_category__category_name=product.product_category.category_name) |
            Q(product_sub_category__sub_category_name=product.product_sub_category.sub_category_name),
            is_draft=False, is_active=True
        ).exclude(id=pk).distinct()

        # If no related products found, fallback to the original queryset.
        if not products:
            products = Product.objects.filter(
                is_draft=False, is_active=True).exclude(id=pk)

        context = {
            'products': products,
            'product': product
        }
        return render(request, 'product-info.html', context)

    except ObjectDoesNotExist as error:
        error_message = str(error)

    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"

    return render(request, 'listed_unlisted_product.html', {'error_message': error_message})
