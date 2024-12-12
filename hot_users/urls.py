from django.urls import path
from .views import create, create_role, login, current_user, get_role, get_all_roles, get_all_users, get_user


urlpatterns = [
    path('login/', login, name='login'),
    path('current/', current_user, name='current_user'),
    path('create/', create, name='create'),
    path('list', get_all_users, name='get_all_users'),
    path('one/<int:idUser>/', get_user, name='get_user'),
    path('role', get_all_roles, name='get_all_roles'),
    path('role/<int:idRole>/', get_role, name='get_role'),
    path('createrole/', create_role, name='create_role'),
]