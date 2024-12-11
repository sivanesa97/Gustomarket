"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Services.models import OrderItem, Supplier, PaymentTerm


@login_required(login_url='sign_in')
def customer_list(request):
    """
    customer_list
    """
    customers = None
    try:
        supplier = Supplier.objects.get(user=request.user)
        order_items = OrderItem.objects.filter(product__supplier=supplier)
        payment_terms = PaymentTerm.objects.all()

        # dictionaries with customers as keys
        # lists of length 2: [total order quantity, customer debts]
        customers = {}
        company_names = {}
        company_logos = {}
        orders = []

        for order_item in order_items:
            customer = order_item.order.customer

            if order_item.order.customer not in customers:
                customers[customer] = [
                    0, order_item.total_price]
                try:
                    customer_company = Supplier.objects.get(user=customer.user).company
                except Supplier.DoesNotExist:
                    customer_company = None
                if customer_company:
                    company_names[customer] = customer_company.company_name
                    url = ""
                    if customer.user.company_set.first():
                        if customer.user.company_set.first().logo:
                            url = customer.user.company_set.first().logo.url
                            if not os.path.exists(url):
                                url = ""
                    company_logos[customer] = url
            else:
                customers[customer][1] += order_item.total_price
            if order_item.order.orderID not in orders:
                customers[customer][0] += 1
                orders.append(order_item.order.orderID)
        print(company_logos)

        context = {
            'customers': customers,
            'company_names': company_names,
            'company_logos': company_logos,
            'payment_terms': payment_terms,
        }
        return render(request, 'customer-list.html', context)

    except Supplier.DoesNotExist:
        error_message = 'Supplier not found'
    except Exception as error:
        # Handle unexpected errors and provide an error message
        error_message = f"An unexpected error occurred: {error}"

    return render(request, 'customer-list.html', {'error_message': error_message})
