"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Services.models.product_order import OrderItem
from Services.models import Supplier, Customer
from Services.views.seller_dashboard import aggregate_sold, aggregate_purchased


@login_required(login_url='sign_in')
def earnings(request):
    """
    earnings
    """
    try:
        supplier = Supplier.objects.get(user=request.user)
        customer = Customer.objects.filter(user=request.user).first()
        sold_items = OrderItem.objects.filter(product__supplier=supplier).select_related('order').order_by('-order__order_date')
        purchased_items = OrderItem.objects.filter(
            order__customer=customer).select_related('order').order_by('-order__order_date')

        '''Creates a list of sublists length 4 [sample item of an orderID, 
        number of items in an order ID, list of products in that orderID, order price]. All items 
        that appear are those sold by the current user. Aggregated by orderID and supplier.
        Also returns dictionary of unique product quantity per orderID and company names of customers. '''
        _, sold_combined, _, customer_names = aggregate_sold(
            sold_items)
        '''Creates a list of sublists of length 4 [sample item of an orderID, 
        number of items in an order ID, list of products in that orderID, order price]. All items that 
        appear are those purchased by the current user. Each sublist is for a different 
        supplier/order ID. Aggregated by orderID and supplier. Also returns dictionary of unique 
        product quantity per orderID.'''
        _, purchased_combined, _ = aggregate_purchased(
            purchased_items)

        context = {
            'sold_combined': sold_combined,
            'purchased_combined': purchased_combined,
            'customer_names': customer_names,
        }

        return render(request, 'earnings.html', context)

    except Supplier.DoesNotExist:
        error_message = 'Supplier not found'
    except Exception as error:
        # Handle unexpected errors and provide an error message
        error_message = f"An unexpected error occurred: {error}"

    return render(request, 'earnings.html', {'error_message': error_message})
