"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import stripe
from Services.models import Supplier


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url='sign_in')
def setup_stripe_connect(request):
    """
    Stripe Connect account setup view
    """
    try:
        supplier = Supplier.objects.get(user=request.user)
        account = stripe.Account.create(
            type="standard",
            country="US",
            email=request.user.email
        )

        # Save the Stripe account ID in the Supplier model
        supplier.stripe_account_id = account.id
        supplier.save()

        # Create an Account Link for the onboarding flow
        account_link = stripe.AccountLink.create(
            account=account.id,
            refresh_url=request.build_absolute_uri(
                reverse('stripe_connect_callback')),
            return_url=request.build_absolute_uri(
                reverse('stripe_connect_callback')),
            type="account_onboarding",
        )

        # Redirect the seller to the Stripe Express onboarding flow
        return redirect(account_link.url)

    except (stripe.error.StripeError, Supplier.DoesNotExist, Exception) as error:
        # Handle errors, log them, and return an error response
        return render(request, 'error_template.html', {'error_message': str(error)})


def stripe_connect_callback(request):
    """
    stripe_connect_callback
    """
    return render(request, 'stripe_connect_callback.html')
