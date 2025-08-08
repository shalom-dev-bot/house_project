
# Register your models here.
from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'address', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('title', 'address', 'description')
