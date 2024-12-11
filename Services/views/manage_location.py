"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
ObjectDoesNotExist : Handling erro when exception occured.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from Services.models import (Profile, Role, Team, Country, Address,
                             State, CustomPermission, LocationType, Seniority, Supplier)


@login_required(login_url='sign_in')
def manage_location(request):
    """
    Process for managing team location as needed.
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
            location_type = LocationType.objects.get(
                id=request.POST.get('location_type_id'))
            location_id = request.POST.get('location_id')

            if location_id:
                address_inst = Address.objects.get(id=location_id)
                address_inst.location_type = location_type
                address_inst.is_active = request.POST.get(
                    'checked', False) == 'on'
                address_inst.save()

                return redirect('manage_team')

            state_inst = State.objects.get(id=request.POST.get('state_id'))
            country_inst = Country.objects.get(
                id=request.POST.get('country_id'))

            address_inst, _ = Address.objects.get_or_create(
                supplier=supplier,
                location=request.POST.get('location'),
                address_lane_1=request.POST.get('address_line_1'),
                address_lane_2=request.POST.get('address_line_2'),
                city=request.POST.get('city'),
                zip_code=request.POST.get('zip_code'),
                state=state_inst,
                country=country_inst,
                location_type=location_type
            )
            address_inst.is_active = True
            address_inst.save()

            return redirect('manage_team')

    except (ObjectDoesNotExist, ValidationError, PermissionDenied, IntegrityError) as error:
        error_message = str(error)
        status_code = 404

    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"
        status_code = 500

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

    return render(
        request,
        'manage-team.html',
        context,
        status=status_code
    )
