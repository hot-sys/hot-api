from django.urls import path
from .views import create, get_all, update, get_by_id, get_all_history, get_history_room, get_all_history_user, get_all_history_by_user

urlpatterns = [
    path('all', get_all_history, name='get_all_history'),
    path('room/<int:idRoom>', get_history_room, name='get_history_room'),
    path('user', get_all_history_user, name='get_all_history_user'),
    path('byuser/<int:idUser>', get_all_history_by_user, name='get_all_history_by_user'),
    path('type/all', get_all, name='get_all'),
    path('type/create', create, name='create'),
    path('type/get/<int:idType>', get_by_id, name='get_by_id'),
    path('type/update/<int:idType>', update, name='update'),
]