"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
login_required : checking a user is authorized or not.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='sign_in')
def join_team(request):
    """
    join_team
    """
    return render(request, 'join-team.html')


@login_required(login_url='sign_in')
def join_team_2(request):
    """
    join_team_2
    """
    return render(request, 'join-team2.html')
