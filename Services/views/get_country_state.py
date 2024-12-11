"""
The modules have imported for different purpose mentioned as below:
JsonResponse : for JsonDta.
"""
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from Services.models import State


def get_country_state(request):
    """
    Get a list of states for a given country using AJAX request.
    """
    try:
        country_id = request.GET.get('country_id')
        states = State.objects.filter(
            country=country_id).values('id', 'state_name')
        return JsonResponse(list(states), safe=False)

    except ObjectDoesNotExist:
        error_message = 'Country not found'
        status = 404

    except Exception as error:
        error_message = f'An unexpected error occurred: {error}'
        status = 500

    return JsonResponse({'error_message': error_message}, status=status)
