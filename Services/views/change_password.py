"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
ValidationError: If the new password does not meet validation criteria.
"""
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from Services.validators.password_validators import regex_password_validator

User = get_user_model()


@login_required(login_url='sign_in')
def change_password(request):
    """
    View for allowing a logged-in user to change their password.
    """
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = User.objects.get(username=request.user)
            is_password_correct = check_password(old_password, user.password)

            if not is_password_correct:
                raise ValidationError("Invalid Credentials.")

            regex_password_validator(new_password)

            if new_password == old_password:
                raise ValidationError(
                    'New password must be different from the old password.')

            if new_password != confirm_password:
                raise ValidationError("Passwords did not match.")

            # If all conditions pass, update the password
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('sign_in')

        except User.DoesNotExist:
            messages.error(request, "User Not Found, Please Try Again.")
        except ValidationError as exception:
            messages.error(request, exception.message)

    return render(request, 'change_password.html', {'email': request.user})
