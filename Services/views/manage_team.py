"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
ObjectDoesNotExist : Handling erro when exception occured.
"""
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from Services.models import Profile
from Services.models import (Role, CustomPermission, LocationType, Seniority, Supplier,
                             Team, Country, State, Address)


@login_required(login_url='sign_in')
def manage_team(request):
    """
    Process profile, role, permission, and location as needed.
    """
    (supplier, location_types, countrys,
     states, profiles, roles, teams, addresses,
     permissions, seniorities, error_message
     ) = [None] * 11
    status_code = 200  # Default status code

    try:
        location_types = LocationType.objects.all()
        countrys = Country.objects.all()
        states = State.objects.all()
        profiles = Profile.objects.all()
        roles = Role.objects.all()
        permissions = CustomPermission.objects.all()
        seniorities = Seniority.objects.all()
        supplier = Supplier.objects.get(user=request.user)
        teams = Team.objects.filter(
            supplier__user=request.user).order_by('-id')
        addresses = Address.objects.filter(
            supplier__user=request.user).order_by('-id')

        if request.method == 'POST':
            team = Team.objects.get(id=request.POST.get('team_id'))

            # Handle profiles, roles, and permissions
            team.profile.set(request.POST.getlist('profile_id'))
            team.role.set(
                [item for item in request.POST.getlist('role_id') if item != 'on'])
            team.permission.set(request.POST.getlist('permission_id'))

            # Handle location and is_active
            address = Address.objects.get(id=request.POST.get('location_id'))
            team.address = address
            team.is_active = request.POST.get('checked', False) == 'on'

            team.save()
            return redirect('manage_team')

    except ObjectDoesNotExist as error:
        error_message = f"Object not found: {error}"
        status_code = 404  # Object not found
    except (ValidationError, PermissionDenied) as error:
        error_message = str(error)
        status_code = 400  # Bad request
    except IntegrityError as error:
        error_message = f"Integrity error: {error}"
        status_code = 500  # Internal server error
    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"
        status_code = 500  # Internal server error

    context = {
        'profiles': profiles,
        'roles': roles,
        'teams': teams,
        'permissions': permissions,
        'addresses': addresses,
        'seniorities': seniorities,
        'error_message': error_message,
        'location_types': location_types,
        'countrys': countrys,
        'supplier': supplier,
        'states': states
    }

    return render(request, 'manage-team.html', context, status=status_code)
