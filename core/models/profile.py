# core/models/profile.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

def user_profile_image_path(instance, filename):
    return f'profiles/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(_("Profile Picture"), upload_to=user_profile_image_path, default='profiles/default.jpg')
    bio = models.TextField(_("Bio"), blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
