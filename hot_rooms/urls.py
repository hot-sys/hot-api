from django.urls import path
from .views import all, getRoom, create

urlpatterns = [
    path('all', all, name='all'),
    path('create', create, name='create'),
    path('get/<int:idRoom>', getRoom, name='getRoom'),
]