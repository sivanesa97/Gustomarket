"""
The modules have imported for different purpose mentioned as below:
JsonResponse : for JsonDta.
"""
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from Services.models import ProductSubCategory


def get_sub_category(request):
    """
    Get a list of sub category for a given category using AJAX request.
    """
    try:
        category_id = request.GET.get('category_id')
        print(category_id)
        sub_category = ProductSubCategory.objects.filter(
            product_category=category_id).values('id', 'sub_category_name')
        return JsonResponse(list(sub_category), safe=False)

    except ObjectDoesNotExist:
        error_message = 'Sub Category not found'
        status = 404

    except Exception as error:
        error_message = f'An unexpected error occurred: {error}'
        status = 500

    return JsonResponse({'error_message': error_message}, status=status)
