"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
get_object_or_404 : getting an object if not getting, then 404 error.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from Services.models import Supplier, Company, CompanyType, LocationType, State, Country, Address


@login_required(login_url='sign_in')
def account_registration(request, editable=None):
    """
    Register a complete supplier profile and its company information.
    """
    (company_types,
     location_types,
     countrys,
     states,
     supplier,
     error_message) = [None] * 6
    try:
        company_types = CompanyType.objects.all()
        location_types = LocationType.objects.all()
        countrys = Country.objects.all()
        states = State.objects.all()
        user = User.objects.get(username=request.user)
        supplier, _ = Supplier.objects.get_or_create(
            user=user, email=request.user.email)

        if request.method == 'POST':
            # Check unique constraint.
            context = custom_validation(request, supplier, company_types,
                                        location_types, countrys, states, editable)
            if context['validation_dict']:
                return render(request, 'account_registration.html', context)

            # Check if a new photo is uploaded
            new_photo = request.FILES.get('photo')
            if new_photo:
                supplier.photo = new_photo

            # Update Supplier profile
            supplier.first_name = request.POST.get('first-name')
            supplier.last_name = request.POST.get('last-name')
            supplier.email = request.POST.get('email')
            supplier.public = request.POST.get('public', False) == 'public'
            supplier.private = request.POST.get('private', False) == 'private'
            supplier.phone = request.POST.get('phone')
            supplier.birth_date = request.POST.get('birth-date')

            # Create or Update company.
            company_instance = create_or_update_company(
                request, supplier, user)
            supplier.company = company_instance
            supplier.is_active = True
            supplier.save()

            return redirect('team_registration')

    except ValidationError as error:
        # Handle validation errors and provide an error message
        error_message = str(error)

    except Exception as error:
        # Handle unexpected errors and provide an error message
        error_message = f"An unexpected error occurred: {error}"

    context = {
        'company_types': company_types,
        'location_types': location_types,
        'countrys': countrys,
        'states': states,
        'supplier': supplier,
        'error_message': error_message,
        'editable': editable
    }
    return render(request, 'account_registration.html', context)


def create_or_update_company(request, supplier, user):
    """
    Update or create a Company Information of a supplier.
    """
    # Get CompanyType instance.
    company_type_inst = CompanyType.objects.get(
        id=request.POST.get('company_type'))

    # Update or create a Company instance of a supplier.
    company_instance, _ = Company.objects.get_or_create(supplier=supplier)
    new_logo = request.FILES.get('logo')
    if new_logo:
        company_instance.logo = new_logo

    company_instance.company_name = request.POST.get('name')
    company_instance.ein = request.POST.get('ein')
    company_instance.signature_code = request.POST.get('code')
    company_instance.company_phone = request.POST.get(
        'company_phone')
    company_instance.company_mobile = request.POST.get('mobile')
    company_instance.website = request.POST.get('website')
    company_instance.company_type = company_type_inst
    company_instance.created_by = user

    # Update or create an address instance of a company.
    address_instance = update_or_create_address(
        request, company_instance, supplier)
    company_instance.address = address_instance
    company_instance.save()

    return company_instance


def update_or_create_address(request, company_instance, supplier):
    """
    Update or create a Address instance of a Company.
    """
    # Get CompanyType, Country, and State instances.
    location_type_inst = LocationType.objects.get(
        id=request.POST.get('location_type'))
    country_inst = Country.objects.get(id=request.POST.get('country'))
    state_inst = State.objects.get(id=request.POST.get('state'))

    # Update or create a Address instance of a Company.
    address_instance, _ = Address.objects.get_or_create(
        company=company_instance)
    address_instance.supplier = supplier
    address_instance.location = request.POST.get('location')
    address_instance.address_lane_1 = request.POST.get(
        'address_lane_1')
    address_instance.address_lane_2 = request.POST.get(
        'address_lane_2')
    address_instance.city = request.POST.get('city')
    address_instance.zip_code = request.POST.get('zip_code')
    address_instance.state = state_inst
    address_instance.country = country_inst
    address_instance.location_type = location_type_inst
    address_instance.save()

    return address_instance


def custom_validation(request, supplier, company_types, location_types, countrys, states, editable):
    """
    Perform Validation on some unique fields of a supplier and its company.
    """
    error_message = {}
    phone = request.POST.get('phone')
    if phone:
        if Supplier.objects.filter(phone=phone).exclude(phone=supplier.phone).exists():
            error_message['supplier_phone_exists'] = 'The phone number already exists.'

    if supplier.company:
        if Company.objects.filter(ein=request.POST.get('ein')).exclude(ein=supplier.company.ein).exists():
            error_message['company_ein_exists'] = 'The EIN is already exists.'

        if Company.objects.filter(signature_code=request.POST.get('code')).exclude(signature_code=supplier.company.signature_code).exists():
            error_message['signature_code_exists'] = 'The signature code is already exists.'

        if Company.objects.filter(company_phone=request.POST.get('company_phone')).exclude(company_phone=supplier.company.company_phone).exists():
            error_message['company_phone_exists'] = 'The phone number you have entered is already exists.'

        if Company.objects.filter(company_mobile=request.POST.get('mobile')).exclude(company_mobile=supplier.company.company_mobile).exists():
            error_message['company_mobile_exists'] = 'The mobile number you have entered is already exists.'

    else:
        if Company.objects.filter(ein=request.POST.get('ein')).exists():
            error_message['company_ein_exists'] = 'The EIN is already exists.'

        if Company.objects.filter(signature_code=request.POST.get('code')).exists():
            error_message['signature_code_exists'] = 'The signature code is already exists.'

        if Company.objects.filter(company_phone=request.POST.get('company_phone')).exists():
            error_message['company_phone_exists'] = 'The phone number you have entered is already exists.'

        if Company.objects.filter(company_mobile=request.POST.get('mobile')).exists():
            error_message['company_mobile_exists'] = 'The mobile number you have entered is already exists.'

    context = {
        'company_types': company_types,
        'location_types': location_types,
        'countrys': countrys,
        'states': states,
        'supplier': supplier,
        'editable': editable,
        'validation_dict': error_message
    }
    return context
