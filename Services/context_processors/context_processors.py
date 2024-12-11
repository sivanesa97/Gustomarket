"""
The modules have imported for different purpose mentioned as below:
"""
from django.conf import settings
from Services.models import Supplier


def language_flags(request):
    """
    language_flags
    """
    return {'LANGUAGE_FLAGS': settings.LANGUAGE_FLAGS}


def profile_picture(request):
    """
    profile_picture
    """
    user_profile = None
    if request.user.is_authenticated:
        user_profile = Supplier.objects.filter(user=request.user).first()

    return {'user_profile': user_profile.photo if user_profile else None}
