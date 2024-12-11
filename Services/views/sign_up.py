"""
The modules have imported for different purpose mentioned as bellow:
render : to render an HTML template.
message : for informing to the user as a message.
send_otp_mail : send otp as email to the user 
"""
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from Services.views.send_mail import generate_otp, send_otp_email
from Services.models import Supplier


def sign_up(request):
    """
    Send OTP to the new user after checking existing user, and registered it
    with the username as email, email as email and password as OTP.
    """
    if request.method == 'POST':
        # Get user data from request
        email = request.POST.get('email')

        try:
            # Check if user with the same username or email already exists
            if User.objects.filter(username=email).exists():
                messages.success(
                    request, "The email you have entered already exists.")
                return render(request, 'signup.html')

            # Generate OTP
            otp = generate_otp()

            # Send OTP via email
            send_otp_email(email, otp)

            # Store email and OTP in session
            request.session['temp_email'] = email
            request.session['temp_otp'] = otp

            return render(request, 'check_email.html', {'email': email})

        except Exception as error:
            messages.error(request, f"An error occurred: {str(error)}")

    return render(request, 'signup.html')
