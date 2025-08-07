from django.urls import path
from . import views
from .views import listings
from .views import about_view

urlpatterns = [
    path('', views.index, name='index'),
     path('listings/', listings, name='listings'),
     path('about/', about_view, name='about'),
]
