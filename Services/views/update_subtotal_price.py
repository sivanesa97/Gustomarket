import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from Services.models import OrderItem

@csrf_protect  # Ensure CSRF protection
def update_subtotal_price(request):
    print("In views.py: update_total_price function")

    if request.method == 'POST':
        data = json.loads(request.body)
        order_item_id = data.get('orderItemId')
        total_price = data.get('totalPrice')

        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            order_item.total_price = total_price
            order_item.save()
            return JsonResponse({'success': True})
        except OrderItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order item not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
