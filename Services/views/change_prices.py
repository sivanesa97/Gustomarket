"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django import template
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decimal import Decimal, ROUND_HALF_UP
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
# from django.core.paginator import Paginator
from Services.models import Supplier, Product, ProductPricingHistory, NotificationPreference
from django.db.models import F

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@login_required(login_url='sign_in')
def change_prices(request):
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
        frequency_choices = NotificationPreference.objects.all()
        now = timezone.now()

        # Filter products based on when last updated

        products_daily = products.filter(
            notification_frequency__iexact='daily - market priced', updated_at__lte=now - timedelta(days=1))
        products_weekly = products.filter(
            notification_frequency__iexact='weekly', updated_at__lte=now - timedelta(weeks=1))
        products_monthly = products.filter(
            notification_frequency__iexact='monthly', updated_at__lte=now - timedelta(days=30))
        products_yearly = products.filter(
            notification_frequency__iexact='yearly', updated_at__lte=now - timedelta(days=365))
        products_just_created = products.filter(
            created_at__gte=now - timedelta(days=1), created_at__date=F('updated_at__date'),
            created_at__hour=F('updated_at__hour'),
            created_at__minute=F('updated_at__minute')
        )

        products = products_daily | products_weekly | products_monthly | products_yearly | products_just_created

        avg_prices = {}
        two_places = Decimal(10) ** -2
        # Calculate the average price for each product
        for product in products:
            if product and product.price_transport:
                pricinghistory = ProductPricingHistory.objects.filter(
                    product=product)
                count = 0
                sum = Decimal(0)
                for update in pricinghistory:
                    sum += Decimal(update.old_price)
                    count += 1
                if count != 0:
                    avg_prices[product.id] = Decimal(
                        sum / count).quantize(two_places, rounding=ROUND_HALF_UP)
                else:
                    avg_prices[product.id] = Decimal(
                        product.price_transport.amount)
        # paginator = Paginator(products, 2)

        if request.method == 'POST':
            # Get the list of selected products
            selected_products = request.POST.getlist('selected_products')

            # Handle different actions based on the 'publish_action' POST parameter
            publish_action = request.POST.get('publish_action')
            new_amounts = request.POST.getlist('price')
            notification_frequencies = request.POST.getlist(
                'notification-frequency')
            print(notification_frequencies)

            if publish_action == 'price_changed':
                # Make selected products in active.
                count = 0
                for product in products:
                    if product and product.price_transport:
                        if str(product.id) in selected_products:
                            # Edit Product Price
                            product.price_transport.amount = Decimal(
                                new_amounts[count])
                            # Edit Product notification_frequency and product packaging notification preference
                            product.notification_frequency = notification_frequencies[count]
                            product.product_packaging.notification_preference, _ = NotificationPreference.objects.get_or_create(
                                frequency=notification_frequencies[
                                    count])
                            product.price_transport.save()
                            product.product_packaging.save()
                            product.save()
                    count += 1

            return HttpResponseRedirect(request.path_info)

    except ObjectDoesNotExist as error:
        error_message = str(error)
    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"

    context = {
        'supplier': supplier,
        'products': products,
        'avg_prices': avg_prices,
        'frequency_choices': frequency_choices,
        'error_message': error_message,
    }
    return render(request, 'change_prices.html', context)
