"""
The modules have imported for different purpose mentioned as bellow:
redirect: redirect to a new page.
logout : Log Out the request
"""
from django.contrib.auth import logout
from django.shortcuts import redirect


def sign_out(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    logout(request)
    return redirect('sign_in')
