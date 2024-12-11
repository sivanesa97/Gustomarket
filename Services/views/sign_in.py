"""
The modules have imported for different purpose mentioned as bellow:
render : to render an HTML template.
authenticate : checking a user is authenticated or not.
login :  Persist a user id and a backend in the request.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


def sign_in(request):
    """
    Log In after checking authentication provided credentials by user,
    if user have registered.

    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # First check if user exists
            user = User.objects.get(username=email)
            
            # Then attempt authentication
            authenticated_user = authenticate(username=email, password=password)
            
            if authenticated_user is not None:
                # Only create changelog entries after successful authentication
                if authenticated_user.last_login is None:
                    login(request, authenticated_user)
                    return redirect('account_registration', editable=None)
                login(request, authenticated_user)
                return redirect('products')
            else:
                messages.error(request, "Incorrect username or password")

        except User.DoesNotExist:
            messages.error(request, "Your account does not exist, please sign up!")

    if request.user.is_authenticated:
        return redirect('account_registration', editable=None)
    return render(request, 'sign_in.html')
