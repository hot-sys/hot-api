from django.urls import path
from .views import create, get_all, update, get_by_id

urlpatterns = [
    path('status/all', get_all, name='get_all'),
    path('status/create', create, name='create'),
    path('status/get/<int:idStatus>', get_by_id, name='get_by_id'),
    path('status/update/<int:idStatus>', update, name='update'),
]