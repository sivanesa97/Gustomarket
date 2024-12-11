"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from Services.views.send_mail import generate_otp, send_pass_email
from Services.models import Supplier, Team, Seniority


@login_required(login_url='sign_in')
def team_registration(request):
    """
    View for registering a team member associated with a supplier.
    """
    (seniorities,
     supplier,
     teams,
     error_message) = [None] * 4
    try:
        seniorities = Seniority.objects.all()
        error_message = None
        status_code = 200
        supplier = Supplier.objects.get(user=request.user)
        teams = Team.objects.filter(supplier=supplier).order_by('-id')

        if request.method == 'POST':
            return_url = request.POST.get('return_url')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            seniority_id = request.POST.get('seniority')

            # Check unique constraint.
            context = custom_validation(phone, email, seniorities, teams)
            if context['validation_dict']:
                if return_url:
                    return render(request, 'manage-team.html', context)
                return render(request, 'team_registration.html', context)

            seniority = Seniority.objects.get(id=seniority_id)
            password = generate_otp()

            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            Team.objects.create(
                user=user,
                supplier=supplier,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                seniority=seniority
            )
            send_pass_email(email, password)

            if return_url:
                return HttpResponseRedirect(return_url)
            return HttpResponseRedirect(request.path_info)

    except ObjectDoesNotExist as error:
        error_message = str(error)
        status_code = 404  # Object not found
    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"
        status_code = 500  # Internal Server Error

    context = {
        'seniorities': seniorities,
        'supplier': supplier,
        'teams': teams,
        'error_message': error_message
    }
    return render(
        request,
        'team_registration.html',
        context,
        status=status_code
    )


def custom_validation(phone, email, seniorities, teams):
    """
    custom_validation
    """
    error_message = {}

    if Team.objects.filter(phone=phone).exists():
        error_message['team_phone_exists'] = 'The phone number is already exists.'

    if Team.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
        error_message['team_email_exists'] = 'The email you have entered is already exists.'

    context = {
        'seniorities': seniorities,
        'teams': teams,
        'validation_dict': error_message
    }
    return context
