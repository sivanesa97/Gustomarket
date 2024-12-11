
"""
# The modules have imported for different purpose mentioned as below:
# render : to render an HTML template.
# login_required : checking a user is authorized or not.
# """
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from Services.models import Supplier
from Services.views.send_mail import send_mail
from django.shortcuts import render, redirect
import re


@login_required(login_url='sign_in')
def help(request):
    email = request.user.email
    if request.method == 'POST':
        try:
            message = request.POST.get('message_content')
            message = re.sub('<.*?>', '', message)
            subject = f'Help Form from {email}'

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      ['fm292@cornell.edu'])
            messages.success(request, 'Message sent.')
        except User.DoesNotExist:
            messages.error(request, 'User not registered.')
        return redirect('help')

    # Redirect to the same page after sending the email
    return render(request, 'help.html', {'email': email})
