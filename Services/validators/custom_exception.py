# """
# The modules have imported to perform validation error.
# """
# from django.core.exceptions import ValidationError


# # custom_exceptions start
# class CustomValidationError(Exception):
#     """Raise Custom Exception"""
#     pass
#     # def __init__(self, message):
#     #     self.message = message
#     #     super().__init__(self.message)
# # custom_exceptions end



# # start Fucntion for raising error during updating
# def check_and_assign_field_value(instance, field_name, new_value, supplier_id):
#     """
#     Checking existence and assign the value if not exists.
#     """
#     existing_supplier = instance.objects.filter(
#         **{field_name: new_value}).exclude(id=supplier_id).exists()

#     if existing_supplier:
#         raise CustomValidationError
#     else:
#         setattr(instance, field_name, new_value)
# # End Fucntion for raising error during updating



# # start Fucntion for raising error during creating
# def check_and_raise_custom_error(model, field, value):
#     """
#     Checking existence and raise the exception if exists.
#     """
#     if model.objects.filter(**{field: value}).exists():
#         raise CustomValidationError
# # End Fucntion for raising error during creating
