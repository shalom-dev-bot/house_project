from django.contrib import admin

# Register your models here
from .models.profile import Profile

admin.site.register(Profile)
