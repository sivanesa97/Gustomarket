"""
Importing models is used for creating a database model.
"""
from django.db import models


class FileType(models.Model):
    """
    A class representing the type of document file.
    """
    file_type_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.file_type_name)



class FileRepository(models.Model):
    """
    A class reprenting the repositary of file.
    """
    file_type_id = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='file_repository/')

    def __str__(self):
        return str(self.code_name)
