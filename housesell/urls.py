from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listings/', views.listings, name='listings'),
    path('about/', views.about_view, name='about'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('add-testimonial/', views.add_testimonial, name='add_testimonial'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('payment/<int:listing_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('search/', views.search_listings, name='search_listings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
