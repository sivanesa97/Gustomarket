"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
get_object_or_404 : getting an object if not getting, then 404 error.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from Services.models import Supplier, TermsConditions


@login_required(login_url='sign_in')
def terms_conditions(request):
    """
    View for handling terms and conditions agreement.
    """
    error_message = None
    supplier = None
    terms = None

    try:
        terms = TermsConditions.objects.first()
        supplier = Supplier.objects.get(user=request.user)

        if request.method == 'POST':
            checked = request.POST.get('checked')

            if checked:
                supplier.is_agreed_terms = True
                supplier.terms_conditions = terms
                supplier.save()
                return render(request, 'thank-you.html', {'terms': terms, 'supplier': supplier})
            messages.error(
                request, "Please check the checkbox to agree to the terms")

    except ObjectDoesNotExist as error:
        error_message = str(error)
    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"

    context = {'terms': terms, 'supplier': supplier,
               'error_message': error_message}
    return render(request, 'terms_conditions.html', context)
