"""
The modules have imported for different purpose mentioned as below:
JsonResponse : for JsonDta.
"""
from django.http import JsonResponse
from Services.models import DocumentType


def get_document_types():
    """
    getting types of document from DocumentType model with the help of Ajax request.
    """
    try:
        document_types = DocumentType.objects.all()
        data = [{'id': document_type.id, 'document_type': document_type.document_type}
                for document_type in document_types]
        return JsonResponse(data, safe=False)

    except DocumentType.DoesNotExist:
        error_message = "Document Type not found"
        status = 404
        return JsonResponse({'error_message': error_message}, status=status)
