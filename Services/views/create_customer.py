"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.models import User
import stripe
from Services.models import Customer, Supplier, Address

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url='login/')
def get_or_create_customer(request):
    """
    Retrieves an existing Stripe customer or creates a new one for the logged-in user.
    """
    try:
        user = User.objects.get(username=request.user.username)
        supplier = Supplier.objects.get(user=user)

        # Try to retrieve the existing customer
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        print("Customer does not exist.")
        # If the customer doesn't exist, create a new one
        stripe_customer = stripe.Customer.create(
            email=request.user.email,
            name=str(supplier.first_name) + " " + str(supplier.last_name),
            phone=supplier.phone if supplier.phone else None,
            # address={
            #     "line1": address.address_lane_1 if address.address_lane_1 else None,
            #     "line2": address.address_lane_2 if address.address_lane_2 else None,
            #     "city": address.city if address.city else None,
            #     "state": address.state.state_name if address.state.state_name else None,
            #     "postal_code": address.zip_code if address.zip_code else None,
            #     "country": address.country.country_name if address.country.country_name else None,
            # },
        )

        try:
            address = Address.objects.get(supplier=supplier)
        except ObjectDoesNotExist:
            return None

        # Update the stripe_customer_id field in the local Customer model
        customer = Customer.objects.create(user=user,
                                           stripe_customer_id=stripe_customer.id,
                                           email=request.user.email,
                                           name=supplier.first_name + " " + supplier.last_name,
                                           phone=supplier.phone,
                                           address=address
                                           )
    return customer
