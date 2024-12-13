from django.urls import path
from .views import all

urlpatterns = [
    path('all', all, name='all'),
]