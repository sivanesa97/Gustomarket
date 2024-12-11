"""
Import re module for doing match a pattern
"""
import re
from django.core.exceptions import ValidationError


def regex_password_validator(password):
    """
    Match password with regex pattern including some conditions
    such as alphanumeric value, upper case, lower case and  special character
    and return a message id condition have not fulfilled.
    """
    regular_expression = r"""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_+=:;'"{}?|,<`~.\]\[ ]).{8,}$"""

    # compiling regex to create regex object
    pattern = re.compile(regular_expression)

    # searching regex
    if not re.search(pattern, password):
        raise ValidationError(
            """Your password must be 8 to 20 characters in length
            and include at least one uppercase letter, one lowercase letter,
            one number, and one special character.""")
