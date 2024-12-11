"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='sign_in')
def payment_registration(request):
    """
    payment_registration
    """
    return render(request, 'payment_registration.html',
                  {'stripe_public_key': settings.STRIPE_PUBLIC_KEY})
