from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import uuid
import json

from .models import Listing, Testimonial, Payment
from accounts.forms import CustomUserCreationForm, TestimonialForm
from accounts.models import Profile

def index(request):
    # Récupérer les 6 dernières propriétés
    latest_listings = Listing.objects.filter(is_available=True).order_by('-created_at')[:6]
    
    # Récupérer les 3 témoignages approuvés
    testimonials = Testimonial.objects.filter(is_approved=True)[:3]
    
    context = {
        'latest_listings': latest_listings,
        'testimonials': testimonials,
    }
    return render(request, 'index.html', context)


def listings(request):
    # Récupérer les paramètres de filtrage
    search_query = request.GET.get('search', '')
    property_type = request.GET.get('property_type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    houses = Listing.objects.filter(is_available=True)
    
    # Appliquer les filtres
    if search_query:
        houses = houses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    if property_type:
        houses = houses.filter(property_type=property_type)
    
    if min_price:
        houses = houses.filter(price__gte=min_price)
    
    if max_price:
        houses = houses.filter(price__lte=max_price)
    
    houses = houses.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(houses, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'houses': page_obj,
        'search_query': search_query,
        'property_type': property_type,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'listings.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # redirige si déjà connecté

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _('Connexion réussie ! Bienvenue sur SellHub.'))
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Compte créé avec succès ! Bienvenue sur SellHub.'))
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, _('Vous avez été déconnecté avec succès.'))
    return redirect('index')

def about_view(request):
    testimonials = Testimonial.objects.filter(is_approved=True)[:6]
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'about.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profil mis à jour avec succès !'))
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'form': form,
        'user_listings': request.user.listings.all(),
        'user_testimonials': request.user.testimonials.all(),
    }
    return render(request, 'profile.html', context)

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, _('Témoignage ajouté avec succès ! Il sera visible après approbation.'))
            return redirect('testimonials')
    else:
        form = TestimonialForm()
    
    return render(request, 'add_testimonial.html', {'form': form})

def testimonials_view(request):
    testimonials = Testimonial.objects.filter(is_approved=True)
    paginator = Paginator(testimonials, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'testimonials': page_obj,
    }
    return render(request, 'testimonials.html', context)

@login_required
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    context = {
        'listing': listing,
    }
    return render(request, 'listing_detail.html', context)

@login_required
def initiate_payment(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, id=listing_id)
        payment_method = request.POST.get('payment_method')
        
        if payment_method not in ['om', 'momo']:
            messages.error(request, _('Méthode de paiement invalide.'))
            return redirect('listing_detail', listing_id=listing_id)
        
        # Créer un nouveau paiement
        payment = Payment.objects.create(
            user=request.user,
            listing=listing,
            amount=listing.price,
            payment_method=payment_method,
            transaction_id=str(uuid.uuid4())
        )
        
        # Ici vous intégreriez l'API de paiement réelle
        # Pour l'instant, on simule un paiement réussi
        payment.is_completed = True
        payment.save()
        
        messages.success(request, _('Paiement initié avec succès !'))
        return redirect('payment_success', payment_id=payment.id)
    
    return redirect('listing_detail', listing_id=listing_id)

@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'payment_success.html', {'payment': payment})

def search_listings(request):
    query = request.GET.get('q', '')
    if query:
        listings = Listing.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query)
        ).filter(is_available=True)[:5]
        
        results = []
        for listing in listings:
            results.append({
                'id': listing.id,
                'title': listing.title,
                'price': str(listing.price),
                'address': listing.address,
                'image_url': listing.image.url if listing.image else '',
            })
        
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})
