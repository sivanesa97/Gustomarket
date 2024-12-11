"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url='sign_in')
def stripe_connect_callback(request):
    """
    Handle Stripe Connect webhook events.
    """
    # Ensure the request is a GET request
    if request.method != 'GET':
        # Redirect to the home page or another appropriate page
        return redirect('team_registration')

    # Extract the state and code parameters from the request
    state = request.GET.get('state')
    code = request.GET.get('code')

    # Verify that the 'state' parameter matches the expected value to prevent CSRF attacks
    if state != 'your_expected_state_value':
        messages.error(request, 'Invalid state parameter. Please try again.')
        # Redirect to the home page or another appropriate page
        return redirect('team_registration')

    try:
        # Use the 'code' parameter to complete the Stripe Connect onboarding process
        response = stripe.OAuth.token(
            grant_type='authorization_code',
            code=code,
        )

        # The 'response' variable contains the access_token and refresh_token
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        
        # You can now save the access_token and refresh_token
        # in your database or associate them with the user

        # Optionally, retrieve the connected account details
        connected_account = stripe.Account.retrieve(access_token)
        # You can store this information in your database or use it for further integration

        messages.success(request, 'Stripe Connect onboarding is complete!')
        # Redirect to the home page or another appropriate page
        return redirect('team_registration')
    except stripe.error.OAuthError as error:
        messages.error(request, f'Stripe Connect onboarding failed: {str(error)}')
        # Redirect to the home page or another appropriate page
        return redirect('team_registration')
