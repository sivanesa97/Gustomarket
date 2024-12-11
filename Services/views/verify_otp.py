"""
The modules have imported for different purpose mentioned as bellow:
render : to render an HTML template.
message : for informing to the user as a message.
check_password : verify plain text password to th user's password.
"""
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages


# Verification process of OTP started here.
def verify_otp(request):
    """
    Get plain OTP and verify it with current user's password.  
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        digits = request.POST.getlist('digit_1')
        digit = ''.join(digits)

        # Retrieve the OTP from the session
        session_otp = request.session.get('temp_otp')

        if session_otp and digit == session_otp:
            # If the OTP matches, proceed to the password setup page
            return render(request, 'security_first.html', {'email': email})

        # If the OTP does not match or is not found in the session
        messages.error(
            request, "The code you have entered is incorrect or has expired. Please try again.")
        return render(request, 'check_email.html', {'email': email})

    return render(request, 'check_email.html')
# OTP verification Ended here.
