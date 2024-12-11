"""
The modules have imported for different purpose mentioned as bellow:
random: generate random number.
send_mail : mail to the user
"""
import random
from django.conf import settings
from django.core.mail import send_mail, EmailMessage


# Start generating 6 digits OTP.
def generate_otp():
    """
    This function generates a six digits number,
    and return as a string.
    """
    return str(random.randint(100000, 999999))
# End OTP generation here.


# start send OTP.
def send_otp_email(email, otp):
    """
    Send email with six digit OTP for user verification purpose.
    """
    subject = 'Your OTP Code'
    message = f'''Your OTP code is: {otp}.
                Please verify first to set a strong password.'''
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)
# End send OTP.


# start send password
def send_pass_email(email, password):
    """
    Send email with six digit password for team credentials.
    """
    subject = 'Your Password'
    message = f'''Your username is: {email},
                and password is: {password},
                You can change your password in future.'''
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)
# End send OTP.


def send_notification_email(email, subject, message, attachment_paths):
    """
    Send email for notification.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list,

    )
    for a in attachment_paths:
        email.attach_file(a)

    email.send()
