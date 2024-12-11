"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from Services.models import Order, OrderItem, Payment  # Cash Payment Code Change (add Payment to here) ----------


@login_required(login_url='login/')
@transaction.atomic
def create_order(request, cart_items, customer):
    """
    create a new order with a unique order id.
    """
    try:
        order_inst = Order.objects.create(customer=customer)
        order_id = f"GM-{str(customer.id)}-{str(order_inst.id)}"

        order_inst.orderID = order_id

        # create order item for each product line items for order.
        create_order_items = add_order_items(order_inst, cart_items)

        order_inst.grand_total = create_order_items[0]
        # order_inst.save()  # Cash Payment Code Change ---------------

        # Set order ID in session
        request.session['order_id'] = order_id

        # Cash Payment Code Changes START ----------------
        payment = Payment.objects.create(paymentID=order_id + "_cashpayment")
        payment.customerID = customer.id
        payment.amount = order_inst.grand_total
        payment.currency = "usd"
        payment.status = "success"
        payment.payment_method_type = "cash"
        payment.save()

        order_inst.payment = payment
        order_inst.save()
        # Cash Payment Code Changes END -------------------

        return order_inst, create_order_items

    except ObjectDoesNotExist as error:
        raise Exception(f"Error retrieving user: {str(error)}")
    except Exception as error:
        raise Exception(f"Error creating order: {str(error)}")


@transaction.atomic
def add_order_items(order_inst, cart_items):
    """
    Add order items to the given order instance.
    """
    grand_total = 0
    line_items = []
    try:
        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            calculate_order = order_calculation(product)
            grand_total += calculate_order['total'] * quantity

            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.product_title,
                    },
                    'unit_amount': int((calculate_order['total']) * 100),
                },
                'quantity': quantity,
            })

            if product:
                order_inst.products.add(product, through_defaults={
                                        'quantity': quantity})

                for _ in range(quantity):
                    OrderItem.objects.create(
                        order=order_inst, product=product,
                        quantity=quantity,
                        subtotal=calculate_order['subtotal'],
                        discount=calculate_order['discount'],
                        tax=calculate_order['tax'],
                        total_fee=calculate_order['total_fee'],
                        total_price=calculate_order['total']
                    )

    except Exception as error:
        raise Exception(f"Error adding order items: {str(error)}")

    return grand_total, line_items


def order_calculation(product):
    """
    Calculate order details based on product and quantity.
    """
    subtotal = Decimal(product.price_transport.amount)
    discount = subtotal * Decimal(product.price_transport.discount) / 100
    discounted_price = subtotal - discount
    tax = discounted_price * Decimal(product.price_transport.tax) / 100
    total_fee = Decimal(product.price_transport.delivery_charge)
    total = discounted_price + tax + total_fee

    context = {'subtotal': subtotal, 'discount': discount,
               'tax': tax, 'total_fee': total_fee, 'total': total}
    return context
