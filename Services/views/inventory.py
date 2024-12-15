from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.db.models import (
    OuterRef, Subquery, Sum, Case, When, Value, 
    CharField, F, IntegerField, Exists, Max, JSONField
)
from django.db.models.functions import JSONObject, Cast
from django.core.serializers.json import DjangoJSONEncoder
from ..models.inventory import InventoryItem, InventoryHistory, InventoryChangeType
from ..models.product import Product
import json
import base64
import uuid
from django.core.files.base import ContentFile

def inventory_list(request):
    change_type_filter = request.GET.get('change_type', None)
    
    # Base queryset with related data
    queryset = InventoryItem.objects.select_related(
        'product', 
        'type_of_change'
    )
    
    # If specific type is selected, show individual entries
    if change_type_filter:
        queryset = queryset.filter(type_of_change_id=change_type_filter)
        items = []
        for item in queryset.order_by('product__product_title', 'type_of_change__name'):
            items.append({
                'product__product_title': item.product.product_title or '',
                'code': item.code or '',
                'current_count': item.new_count,
                'type_of_change__name': item.type_of_change.name if item.type_of_change else '',
                'type_of_change_id': item.type_of_change.id if item.type_of_change else None,
                'product_id': item.product.id,
                'last_updated': item.updated_at,
                'notes': item.notes or ''
            })
    else:
        # For "All Products", group by product and calculate sum based on type status
        from django.db.models import Sum, Q
        
        # Get all products that have inventory items
        products = Product.objects.filter(
            id__in=queryset.values('product_id').distinct()
        ).order_by('product_title')
        
        items = []
        for product in products:
            product_items = queryset.filter(product=product)
            
            # Calculate total based on type_of_change status
            total_count = 0
            for item in product_items:
                if item.type_of_change.change_status == 1:  # Addition
                    total_count += item.new_count
                elif item.type_of_change.change_status == -1:  # Subtraction
                    total_count -= item.new_count
                # If status is 0, don't add to total
            
            # Get the latest updated item for this product
            latest_item = product_items.order_by('-updated_at').first()
            
            items.append({
                'product__product_title': product.product_title,
                'code': latest_item.code if latest_item else '',
                'current_count': total_count,
                'type_of_change__name': 'All Types',  # Since this is grouped view
                'type_of_change_id': None,
                'product_id': product.id,
                'last_updated': latest_item.updated_at if latest_item else None,
                'notes': ''  # Empty notes for grouped view
            })

    return render(request, 'inventory_list.html', {
        'items': items,
        'change_types': InventoryChangeType.objects.all(),
        'selected_change_type': change_type_filter,
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
    """
    Get history for a product across all inventory items.
    Filter by type_of_change if specified.
    """
    # Get the type filter from request parameters
    type_filter = request.GET.get('type_id')
    
    # Build the base query
    query = InventoryHistory.objects.filter(
        inventory_item__product_id=id
    ).select_related('type_of_change', 'inventory_item')
    
    # Apply type filter if specified
    if type_filter:
        query = query.filter(type_of_change_id=type_filter)
    
    # Order by most recent first
    histories = query.order_by('-created_at')
    
    data = []
    for history in histories:
        data.append({
            'created_at': history.created_at.isoformat(),
            'previous_count': history.previous_count,
            'new_count': history.new_count,
            'type_of_change': history.type_of_change.name if history.type_of_change else '',
            'notes': history.notes,
            'picture_url': history.picture.url if history.picture else None
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
            new_count=request.POST.get('new_qty'),
            type_of_change_id=request.POST.get('type_of_change'),  # Add type of change
            notes=request.POST.get('notes'),
            picture=request.FILES.get('picture')  # Save image if provided
        )

        # Update existing inventory item
        inventory_item.count = request.POST.get('count')
        inventory_item.new_count = request.POST.get('new_qty')
        inventory_item.type_of_change_id = request.POST.get('type_of_change')
        inventory_item.notes = request.POST.get('notes')
        
        if 'picture' in request.FILES:
            inventory_item.picture = request.FILES['picture']  # Save the uploaded picture
        
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
        
        # Sort updates by product_id and type_of_change to prevent deadlocks
        updates.sort(key=lambda x: (x.get('product_id'), x.get('type_of_change')))
        
        with transaction.atomic():
            for update in updates:
                product_id = update.get('product_id')
                new_qty = update.get('current_qty', 0) + update.get('new_qty')
                current_qty = update.get('current_qty', 0)
                code = update.get('code')
                type_of_change_id = update.get('type_of_change')
                notes = update.get('notes')
                picture_data = update.get('picture')

                # Process image if provided
                picture = None
                if picture_data and ';base64,' in picture_data:
                    format, imgstr = picture_data.split(';base64,')
                    ext = format.split('/')[-1]
                    picture = ContentFile(
                        base64.b64decode(imgstr), 
                        name=f'inventory_{uuid.uuid4()}.{ext}'
                    )

                # Get or create inventory item with select_for_update
                inventory_item = InventoryItem.objects.select_for_update().filter(
                    product_id=product_id,
                    type_of_change_id=type_of_change_id
                ).first()

                if not inventory_item:
                    # Create new inventory item if it doesn't exist
                    inventory_item = InventoryItem.objects.create(
                        product_id=product_id,
                        type_of_change_id=type_of_change_id,
                        code=code,
                        count=current_qty,
                        new_count=new_qty,
                        notes=notes
                    )
                    previous_count = 0
                else:
                    previous_count = inventory_item.new_count
                    # Update existing inventory item
                    inventory_item.code = code
                    inventory_item.count = current_qty
                    inventory_item.new_count = new_qty
                    inventory_item.notes = notes
                    inventory_item.save()

                # Create single history record with type_of_change_id
                InventoryHistory.objects.create(
                    inventory_item=inventory_item,
                    product_id=product_id,
                    previous_count=previous_count,
                    new_count=new_qty,
                    type_of_change_id=type_of_change_id,  # Add type_of_change_id here
                    notes=notes,
                    picture=picture
                )
        
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        print(f"Error in bulk_update_inventory: {str(e)}")
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
    # Get products with their inventory information grouped by type_of_change
    products = Product.objects.all().annotate(
        inventory_count=Subquery(
            InventoryItem.objects.filter(
                product=OuterRef('pk')
            ).values('new_count')[:1]
        ),
        inventory_code=Subquery(
            InventoryItem.objects.filter(
                product=OuterRef('pk')
            ).values('code')[:1]
        ),
        type_counts=Subquery(
            InventoryItem.objects.filter(
                product=OuterRef('pk')
            ).values('product')
            .annotate(
                type_info=JSONObject(
                    type_name=F('type_of_change__name'),
                    count=Cast('new_count', output_field=IntegerField())
                )
            )
            .values('type_info')[:1]
        )
    )

    # Convert type_counts to proper JSON string for each product
    products_data = []
    for product in products:
        type_counts_json = json.dumps(product.type_counts) if product.type_counts else '{}'
        products_data.append({
            'id': product.id,
            'product_title': product.product_title,
            'inventory_count': product.inventory_count or 0,
            'inventory_code': product.inventory_code or '',
            'type_counts': type_counts_json
        })

    context = {
        'products': products_data,
        'change_types': InventoryChangeType.objects.all(),
    }
    return render(request, 'add_inventory.html', context)

@require_http_methods(["GET"])
def get_current_count(request, product_id, type_id):
    """
    Get the current count for a specific product and type.
    """
    try:
        inventory_item = InventoryItem.objects.filter(
            product_id=product_id,
            type_of_change_id=type_id
        ).first()
        
        current_count = inventory_item.new_count if inventory_item else 0
        
        return JsonResponse({
            'current_count': current_count
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)
