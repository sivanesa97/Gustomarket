"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
import stripe
from django.http import JsonResponse
from django.conf import settings
from django.db.models import ObjectDoesNotExist
from Services.models import Cart
from Services.views.create_customer import get_or_create_customer
from Services.views.create_order import create_order

stripe.api_key = settings.STRIPE_PUBLIC_KEY


def create_checkout_session(request):
    """
    Create a Checkout Session using Stripe.
    """
    try:
        # Fetch products from the user's cart
        cart_items = Cart.objects.filter(user=request.user)

        print("Checkout session request: ", request.user)
        # Retrieve or create a customer
        customer = get_or_create_customer(request)
        if customer is None:
            print("JSON error for no address during customer creation.")
            return JsonResponse({'error': "Please complete your profile with name and address information before purchasing a product."})
        # Create an order
        order_data = create_order(request, cart_items, customer)
        order_inst = order_data[0]

        # Cash Payment Code Changes START ----------------
        if str(request.GET.get("type")) == "stripe":
            session = stripe.checkout.Session.create(
                mode="payment",
                customer=customer.stripe_customer_id,
                invoice_creation={"enabled": True},
                payment_method_types=["us_bank_account"],
                payment_method_options={
                    "us_bank_account": {"financial_connections": {"permissions": ["payment_method"]}},
                },
                line_items=order_data[1][1],
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
                metadata={
                    "order_id": order_inst.orderID,
                },
            )
            return JsonResponse({'session_id': session.id})
        else:
            return JsonResponse({'msg': "success"})

    except stripe.error.StripeError as error:
        print(str(error))
        return JsonResponse({'error': str(error)})
