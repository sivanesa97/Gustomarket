"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
message : for informing to the user as a message.
send_otp_mail : send otp as email to the user 
"""
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from Services.views.send_mail import generate_otp, send_otp_email


# Start resending OTP to the user for email verification.
def resend_otp(request):
    """
    Resend OTP if user exist and set password in place of old OTP
    with the new OTP as a password.
    """
    if request.method == 'POST':

        email = request.POST.get('email')
        try:
            user = User.objects.get(username=email)
            otp = generate_otp() # generate a six digit OTP.
            send_otp_email(email, otp) # mail OTP.
            user.password = make_password(otp)  # Hash the OTP
            user.save()
            # return render(request, 'check_email.html', {'email': email})
        except User.DoesNotExist:
            messages.error(request, "OTP not found, Please send a new OTP.")
        return render(request, 'check_email.html', {'email': email})

    return render(request, 'check_email.html')
# End resending OTP here.
