from django.urls import path
from .views import create, get_all, update, get_by_id, get_all_history

urlpatterns = [
    path('all', get_all_history, name='get_all_history'),
    path('type/all', get_all, name='get_all'),
    path('type/create', create, name='create'),
    path('type/get/<int:idType>', get_by_id, name='get_by_id'),
    path('type/update/<int:idType>', update, name='update'),
]