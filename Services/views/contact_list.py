"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='sign_in')
def contact_list(request):
    """
    contact_list
    """
    return render(request, 'contact_list.html')
