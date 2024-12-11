"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
ValidationError: If the new password does not meet validation criteria.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Services.models import Supplier


@login_required(login_url='sign_in')
def approved_supplier(request):
    """
    View function to retrieve and display approved suppliers.
    Retrieves suppliers excluding those with a null first name.
    """
    try:
        suppliers = Supplier.objects.filter(is_active=True)
        return render(request, 'supplier-list.html', {'suppliers': suppliers})

    except Supplier.DoesNotExist:
        return render(request, 'supplier-list.html', {'error_message': 'Suppliers not found'})
