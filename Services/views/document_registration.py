"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
get_object_or_404 : getting an object if not getting, then 404 error.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Services.models import CompanyRegistrationFile, Supplier, DocumentType, LicenseCertificate


@login_required(login_url='sign_in')
def document_registration(request):
    """
    Functionality for saving uploaded legal documents.
    """
    error_message = None
    supplier = None
    try:
        supplier = Supplier.objects.get(user=request.user)

        if request.method == 'POST':
            documents = request.FILES.getlist('document')
            document_ids = request.POST.getlist('document_id')

            documents1 = request.FILES.getlist('document1')
            document_ids1 = request.POST.getlist('document_id1')

            for doc, doc_id in zip(documents, document_ids):
                document_type = DocumentType.objects.get(id=doc_id)
                instance = CompanyRegistrationFile(
                    company_registration_file=doc,
                    document_type=document_type,
                    supplier=supplier
                )
                instance.save()

            for doc1, doc_id1 in zip(documents1, document_ids1):
                document_type1 = DocumentType.objects.get(id=doc_id1)
                instance1 = LicenseCertificate(
                    license_certificate=doc1,
                    document_type=document_type1,
                    supplier=supplier
                )
                instance1.save()

            return redirect('terms_conditions')

    except Exception as error:
        error_message = f"An unexpected error occurred: {error}"

    return render(
        request,
        'document_registration.html',
        {'supplier': supplier, 'error_message': error_message}
    )
