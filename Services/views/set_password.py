"""
The modules have imported for different purpose mentioned as bellow:
render : to render an HTML template.
message : for informing to the user as a message.
regex_password_validator : Validate password.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Services.models import Supplier
from django.contrib import messages
from django.core.exceptions import ValidationError
from Services.validators.password_validators import regex_password_validator


# Set password in place of OTP start here
def set_password(request):
    """
    Set the user's password after validating the password by confirming both
    password and confirm password are same are not. 
    """
    email = None  # Initialize email outside of the conditional block
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        temp_email = request.session.get('temp_email')
        temp_otp = request.session.get('temp_otp')

        try:
            regex_password_validator(password)  # Validate the password
            if password == confirm_password:
                if temp_email and temp_email == email:
                    new_user = User.objects.create_user(
                        username=email, email=email, password=password)
                    Supplier.objects.create(user=new_user, email=email)

                    # Clear the session
                    del request.session['temp_email']
                    del request.session['temp_otp']
                else:
                    user = User.objects.get(username=email)
                    user.set_password(password)
                    user.save()
                return redirect('sign_in')

            messages.error(request, "Password did not match.")

        except User.DoesNotExist:
            messages.error(request, "User not found, Please sign up again.")

        except ValidationError as exception:
            messages.error(request, exception.message)

    # This block will handle GET requests and invalid POST requests
    return render(request, 'security_first.html', {'email': email})
# Set password end here
