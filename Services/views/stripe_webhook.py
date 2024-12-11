"""
# The modules have imported for different purpose mentioned as below:
# """
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
import stripe
from Services.models import Payment, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Handle successful payment events in a webhook.

    This webhook processes three types of events: 'payment_intent.succeeded',
    'charge.succeeded', and 'checkout.session.completed'.
    For 'payment_intent.succeeded', it updates or creates a Payment object
    and associates it with an existing or new Order.
    For 'charge.succeeded', it updates ACH payment information in the Payment object
    and marks the associated Order as paid.
    For 'checkout.session.completed', it sends an email notification to the customer.
    """
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            # Handle the checkout.session.completed event
            handle_checkout_session_completed(session)

            customer_email = session["customer_details"]["email"]
            send_mail(
                subject='Your Order',
                message="Your order has been placed successfully.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
            )

        elif event["type"] == "payment_intent.succeeded":
            payment_intent = event['data']['object']

            # Handle the payment_intent.succeeded event
            handle_payment_succeeded(payment_intent)

        elif event['type'] == 'charge.succeeded':
            payment_intent = event['data']['object']

            # Handle the charge.succeeded event
            handle_charge_succeeded(payment_intent)

        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']

            # Handle the payment_intent.payment_failed event
            handle_payment_failed(payment_intent)

        else:
            raise ValueError('Unhandled event type: {}'.format(event['type']))

    except ValueError as error:
        return JsonResponse({'error': str(error), 'message': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as error:
        return JsonResponse({'error': str(error), 'message': 'Invalid signature'}, status=400)
    except stripe.error.StripeError as error:
        return JsonResponse({'error': str(error), 'message': 'Stripe error'}, status=400)
    except Exception as error:
        return JsonResponse({'error': str(error), 'message': 'Unexpected error'}, status=400)

    return JsonResponse({'status': 'success'}, status=200)


def handle_checkout_session_completed(session):
    """
    it creates a Payment object and associates it with an existing or new Order.
    """
    order_id = session['metadata']['order_id']
    payment_id = session.get('payment_intent')

    # creating Payment objects.
    payment = Payment.objects.create(paymentID=payment_id)

    payment.customerID = session.get("customer")
    payment.amount = session.get('amount_total') / 100
    payment.currency = session.get("currency")
    payment.status = session.get("payment_status")
    payment.payment_method_type = session.get(
        "payment_method_types")[0]
    payment.save()

    # Retrive the order object with unique order ID.
    order = Order.objects.get(orderID=order_id)
    order.payment = payment
    order.save()

    # Retrieve items from the order
    order_items = OrderItem.objects.get(orderID=order_id)
    charge_id = stripe.PaymentIntent.retrieve(payment_intent.get('payment_intent'))['latest_charge']
    
    seller_payouts = {}
    for item in order_items:
        # STRIPE FLOW ADD ---------------
        product = item.product
        quantity = item.quantity
        total_price = Decimal(
            product.price_transport.amount) * Decimal(quantity)
        current_seller = product.supplier.stripe_account_id
        if current_seller not in seller_payouts.keys(): seller_payouts[current_seller] = {"amt": 0, "purpose": ""}
        seller_payouts[current_seller]["amt"] += total_price
        seller_payouts[current_seller]["purpose"] += str(quantity) + " " + str(product.product_title) + ", "
        # -------------------------------
        
    # STRIPE FLOW ADD ------------------
    # Pay sellers - one transfer object per seller
    for seller in seller_payouts.keys():
        cur_amt = seller_payouts[seller]["amt"] * Decimal(1 - settings.GUSTOMARKET_FEE) + Decimal(0.5) # Add 0.5 is for rounding purposes
        cur_purpose = seller_payouts[seller]["purpose"].removesuffix(", ")
        stripe.Transfer.create(
            amount=int(cur_amt),
            currency="usd",
            destination=seller,
            transfer_group=order_id,
            source_transaction=charge_id,
            metadata={"purpose": cur_purpose}
        )
    # -----------------------------------



def handle_payment_succeeded(payment_intent):
    """
    it updates a Payment object and associates it with an existing or new Order
    """
    payment = Payment.objects.get(paymentID=payment_intent.get('id'))
    payment.status = payment_intent.get("status")
    payment.save()


def handle_charge_succeeded(payment_intent):
    """
    it updates ACH payment information in the Payment object and marks the associated Order as paid.
    """
    payment = Payment.objects.get(
        paymentID=payment_intent.get('payment_intent'))

    ach_payment_info = payment_intent.get(
        'payment_method_details').get('us_bank_account')

    payment.bank_name = ach_payment_info.get('bank_name')
    payment.account_type = ach_payment_info.get('account_type')
    payment.account_holder_type = ach_payment_info.get(
        'account_holder_type')
    payment.account_number_last_4 = ach_payment_info.get('last4')
    payment.routing_number = ach_payment_info.get('routing_number')
    payment.save()

    # Retrive the order object with unique order ID.
    order = Order.objects.get(payment=payment)
    order.payment_status = 'success'
    order.is_paid = True
    order.save()



def handle_payment_failed(payment_intent):
    """
    it updates ACH payment information in the Payment object and marks the associated Order as failed.
    """
    payment = Payment.objects.get(paymentID=payment_intent.get('id'))

    payment.status = 'Failed'
    ach_payment_info = payment_intent.get('last_payment_error').get(
        'payment_method').get('us_bank_account')

    payment.bank_name = ach_payment_info.get('bank_name')
    payment.account_type = ach_payment_info.get('account_type')
    payment.account_holder_type = ach_payment_info.get(
        'account_holder_type')
    payment.account_number_last_4 = ach_payment_info.get('last4')
    payment.routing_number = ach_payment_info.get('routing_number')
    payment.save()

    # Retrive the order object with unique order ID.
    order = Order.objects.get(payment=payment)
    order.payment_status = 'failed'
    order.is_paid = False
    order.save()
