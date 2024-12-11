"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from Services.validators.password_validators import regex_password_validator


# ********************Start handling the process of password reset *****************
def forgot_password(request):
    """
    Handles the process of initiating a password reset.
    """
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_message = 'No user found with this email address.'
            return render(request, 'sign_in.html', {'error_message': error_message})

        # Generate reset token and send email
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = reverse('forgot_password_confirm', kwargs={
                            'uidb64': uidb64, 'token': token})
        reset_url = request.build_absolute_uri(reset_url)
        subject = 'Password Reset Instructions'
        message = f'Click the following link to reset your password:\n\n{reset_url}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return render(request, 'forgot_password.html', {'email': email})

    return render(request, 'forgot_password.html')
# *************** End handling the process of password reset **************************


# *****************Start handling the confirmation of password reset process **********
def forgot_password_confirm(request, uidb64, token):
    """
    Handles the confirmation and completion of the password reset process.

    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return render(request, 'forgot_password_confirm.html', {'validlink': False})

    # Token is valid, proceed with password reset
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            regex_password_validator(new_password)
            if new_password != confirm_password:
                raise ValidationError("Passwords did not match.")

            # If all conditions pass, update the password
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            return render(request, 'forgot_password_confirm.html', {'reset_done': 'reset_done'})

        except ValidationError as exception:
            messages.error(request, exception.message)

    return render(request, 'forgot_password_confirm.html',
                  {'validlink': True, 'uidb64': uidb64, 'token': token})
# ***************** Start handling the confirmation of password reset process ******************
