from django.shortcuts import render
from .models import Listing
def index(request):
    return render(request, 'index.html')


def listings(request):
    houses = Listing.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'listings.html', {'houses': houses})
