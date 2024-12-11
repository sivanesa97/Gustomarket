"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from decimal import Decimal
from django.db import transaction


@transaction.atomic
def calculate_cart(cart_items):
    """
    Calculate cart details such as subtotal, tax, discount, and total.
    """
    try:
        vendors = {}
        grand_total = 0

        for cart_item in cart_items:
            cart_item_id = cart_item.id
            product = cart_item.product
            quantity = cart_item.quantity
            total_price = Decimal(
                product.price_transport.amount) * Decimal(quantity)
            supplier = product.supplier

            if supplier not in vendors:
                vendors[supplier] = {
                    'products': [],
                    'subtotal': Decimal(0),
                    'tax': Decimal(0),
                    'discount': Decimal(0),
                    'total': Decimal(0),
                    'delivery_fee': Decimal(0)
                }

            vendors[supplier]['products'].append(
                (cart_item_id, product, quantity, total_price))

        for supplier, data in vendors.items():
            data['subtotal'] = sum(
                Decimal(product.price_transport.amount) * Decimal(quantity)
                for _, product, quantity, _ in data['products']
            )
            data['discount'] = sum(
                (Decimal(product.price_transport.amount) *
                 Decimal(product.price_transport.discount)/100) *
                Decimal(quantity)
                for _, product, quantity, _ in data['products']
            )
            data['delivery_fee'] = sum(
                Decimal(product.price_transport.delivery_charge) *
                Decimal(quantity)
                for _, product, quantity, _ in data['products']
            )
            discounted_value = sum(
                Decimal(product.price_transport.amount) *
                (1 - Decimal(product.price_transport.discount) / 100) *
                Decimal(quantity)
                for _, product, quantity, _ in data['products']
            )

            total_tax = 0
            for _, product, quantity, _ in data['products']:
                discount = Decimal(product.price_transport.amount) * \
                    (1 - Decimal(product.price_transport.discount) / 100)
                tax = (
                    discount * Decimal(product.price_transport.tax) / 100) * quantity
                total_tax += tax

            data['tax'] = round(total_tax, 2)
            data['total'] = round(
                discounted_value + total_tax + data['delivery_fee'], 2)
            grand_total += data['total']

    except Exception as error:
        # Handle exceptions here, you can print an error message or log the exception
        print(f"Error in calculate_cart: {error}")
        return None

    return vendors, round(grand_total, 2)