from django.http import JsonResponse
from ..models.product import Product
import logging

logger = logging.getLogger(__name__)

def search_products(request):
    query = request.GET.get('term', '')
    logger.info(f"Search query: {query}")
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(product_title__icontains=query)
    logger.info(f"Found {products.count()} products")
    
    results = [{'id': p.id, 'text': p.product_title} for p in products]
    logger.info(f"Results: {results}")
    
    return JsonResponse({'results': results}) 