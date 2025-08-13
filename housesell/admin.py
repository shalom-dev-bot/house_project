
# Register your models here.
from django.contrib import admin
from .models import Listing, Testimonial, Payment

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'property_type', 'is_available', 'owner', 'created_at')
    list_filter = ('property_type', 'is_available', 'created_at')
    search_fields = ('title', 'description', 'address')
    list_editable = ('is_available', 'price')
    date_hierarchy = 'created_at'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__username', 'content')
    list_editable = ('is_approved',)
    date_hierarchy = 'created_at'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'amount', 'payment_method', 'is_completed', 'created_at')
    list_filter = ('payment_method', 'is_completed', 'created_at')
    search_fields = ('user__username', 'transaction_id')
    list_editable = ('is_completed',)
    date_hierarchy = 'created_at'
