"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='sign_in')
def credit_notes(request):
    """
    credit_notes
    """
    return render(request, 'notes-credit.html')
