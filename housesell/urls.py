from django.urls import path
from . import views
from .views import listings


urlpatterns = [
    path('', views.index, name='index'),
]
urlpatterns = [
    path('listings/', listings, name='listings'),
]
