"""
The modules have imported for different purpose mentioned as below:
render : to render an HTML template.
"""
from django.shortcuts import render


def custom_404(request, exception):
    """
    Render to a custom error page if an url is not exists.
    """
    return render(request, 'error_404.html', status=404)
