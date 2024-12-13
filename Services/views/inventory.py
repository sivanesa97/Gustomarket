from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.db.models import OuterRef, Subquery, Sum, Case, When, Value, CharField, F
from ..models.inventory import InventoryItem, InventoryHistory, InventoryChangeType
from ..models.product import Product
import json

def inventory_list(request):
    # Get all products with their latest inventory counts and codes
    products = Product.objects.filter(is_active=True).annotate(
        inventory_count=Sum(
            Case(
                When(inventoryitem__new_count__isnull=False, then='inventoryitem__new_count'),
                default=Value(0),
                output_field=CharField(),
            )
        ),
        inventory_code=Subquery(
            InventoryItem.objects.filter(product=OuterRef('pk')).values('code')[:1]
        ),
        type_of_change=Subquery(
            InventoryItem.objects.filter(product=OuterRef('pk')).values('type_of_change')[:1]
        ),
        status=Case(
            When(inventoryitem__new_count__gt=F('inventoryitem__count'), then=Value('plus')),
            When(inventoryitem__new_count__lt=F('inventoryitem__count'), then=Value('minus')),
            default=Value('no change'),
            output_field=CharField(),
        )
    ).order_by('product_title')

    # Get existing inventory items for the main list
    items = InventoryItem.objects.select_related('product', 'type_of_change').all().order_by('-updated_at')

    change_types = InventoryChangeType.objects.all()

    return render(request, 'inventory_list.html', {
        'items': items,
        'products': products,
        'change_types': change_types,
    })

@require_http_methods(["GET"])
def get_inventory(request, id):
    item = get_object_or_404(InventoryItem, pk=id)
    data = {
        'product_id': item.product.id,
        'product_title': item.product.product_title,
        'product_code': item.code,
        'count': item.count,
        'new_count': item.new_count,
        'type_of_change_id': item.type_of_change.id if item.type_of_change else None,
        'notes': item.notes,
    }
    return JsonResponse(data)

@require_http_methods(["GET"])
def get_inventory_history(request, id):
    histories = InventoryHistory.objects.filter(
        inventory_item_id=id
    ).select_related('type_of_change').order_by('-created_at')
    
    data = []
    for history in histories:
        data.append({
            'created_at': history.created_at.isoformat(),
            'previous_count': history.previous_count,
            'new_count': history.new_count,
            'type_of_change': history.type_of_change.name if history.type_of_change else '',
            'notes': history.notes,
        })
    return JsonResponse(data, safe=False)

@require_http_methods(["POST"])
@transaction.atomic
def update_inventory(request, id):
    try:
        inventory_item, created = InventoryItem.objects.get_or_create(
            product_id=request.POST.get('product_id'),
            code=request.POST.get('code'),
            defaults={
                'count': request.POST.get('count'),
                'new_count': request.POST.get('new_count'),
                'type_of_change_id': request.POST.get('type_of_change'),
                'notes': request.POST.get('notes'),
            }
        )

        # Create history record
        InventoryHistory.objects.create(
            inventory_item=inventory_item,
            previous_count=inventory_item.count,
            new_count=request.POST.get('new_count'),
            type_of_change_id=request.POST.get('type_of_change'),
            notes=request.POST.get('notes'),
            picture=request.FILES.get('picture')  # Save image if provided
        )

        # Update existing inventory item
        inventory_item.count = request.POST.get('count')
        inventory_item.new_count = request.POST.get('new_count')
        inventory_item.type_of_change_id = request.POST.get('type_of_change')
        inventory_item.notes = request.POST.get('notes')
        
        if 'picture' in request.FILES:
            inventory_item.picture = request.FILES['picture']
        
        inventory_item.save()

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_http_methods(["POST"])
@transaction.atomic
def bulk_update_inventory(request):
    try:
        data = json.loads(request.body)
        updates = data.get('updates', [])
        
        for update in updates:
            product_id = update.get('product_id')
            new_qty = update.get('new_qty')
            current_qty = update.get('current_qty', 0)
            code = update.get('code')
            type_of_change_id = update.get('type_of_change')
            
            # Get or create inventory item
            inventory_item, created = InventoryItem.objects.get_or_create(
                product_id=product_id,
                defaults={
                    'code': code,
                    'count': current_qty,
                    'new_count': new_qty,
                    'type_of_change_id': type_of_change_id
                }
            )
            
            if not created:
                # Create history record
                InventoryHistory.objects.create(
                    inventory_item=inventory_item,
                    previous_count=inventory_item.new_count,
                    new_count=new_qty,
                    type_of_change_id=type_of_change_id
                )
                
                # Update existing inventory
                inventory_item.code = code
                inventory_item.count = current_qty
                inventory_item.new_count = new_qty
                inventory_item.type_of_change_id = type_of_change_id
                inventory_item.save()
        
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_http_methods(["GET"])
def get_adjustment_report(request):
    try:
        # Get all inventory items with changes
        items = InventoryItem.objects.select_related(
            'product', 
            'type_of_change'
        ).exclude(
            count=OuterRef('new_count')  # Only get items where count differs from new_count
        ).order_by('product__product_title')
        
        report_data = []
        for item in items:
            report_data.append({
                'product': item.product.product_title,
                'code': item.code,
                'current_qty': item.count,
                'new_qty': item.new_count,
                'difference': item.new_count - item.count,
                'type_of_change': item.type_of_change.name if item.type_of_change else None
            })
            
        return JsonResponse({
            'status': 'success',
            'data': report_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def add_inventory(request):
    products = Product.objects.all()
    
    # Fetch inventory items to get current stock and code
    inventory_items = InventoryItem.objects.all()

    context = {
        'products': products,
        'change_types': InventoryChangeType.objects.all(),
        'inventory_items': inventory_items,
    }
    return render(request, 'add_inventory.html', context)
