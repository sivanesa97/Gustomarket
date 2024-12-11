"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.db.models import Q
from Services.models import Product, ProductAttribute

def purchases(request):
    """
    Displays a list of products for purchase.
    """
    products = None
    message = ""
    error_message = None
    search_value = request.GET.get('search')
    not_found = "No products found matching your search criteria."

    try:
        queryset = Product.objects.filter(is_draft=False, is_active=True)

        if search_value and len(search_value) > 2:

            # Try searching for the full sentence
            products = queryset.filter(
                Q(product_title__icontains=search_value) |
                Q(product_category__category_name__icontains=search_value) |
                Q(product_sub_category__sub_category_name__icontains=search_value) |
                Q(product_attribute__in=ProductAttribute.objects.filter(attribute_name__icontains=search_value)) |
                Q(description__icontains=search_value)
            ).distinct()

            # If no results are found, split the search value and search for each term
            if not products:
                # Split the search value by space
                search_terms = search_value.split()

                # Create a Q object for each search term and combine them using OR
                search_filters = Q()
                for term in search_terms:
                    search_filters |= (
                        Q(product_title__icontains=term) |
                        Q(product_category__category_name__icontains=term) |
                        Q(product_sub_category__sub_category_name__icontains=term) |
                        Q(product_attribute__in=ProductAttribute.objects.filter(attribute_name__icontains=search_value)) |
                        Q(description__icontains=term)
                    )

                # Apply the filters to the queryset
                products = queryset.filter(search_filters).distinct()

                if not products:
                    message = not_found

        elif search_value and len(search_value) < 3:
            message = not_found

        else:
            products = queryset

    except Product.DoesNotExist as error:
        error_message = str(error)
        
    context = {
        'products': products,
        'error_message': error_message,
        'message': message
    }
    return render(request, 'purchases.html', context)
