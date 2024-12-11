"""
Importing models is used for creating a database model.
"""
from django.db import models


class DocumentType(models.Model):
    """
    A class representing the type of the document file.
    """
    document_type = models.CharField(max_length=100, blank=True, null=True)

    # Return object name as a country name
    def __str__(self):
        return str(self.document_type)
