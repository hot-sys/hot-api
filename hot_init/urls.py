from django.urls import path
from .views import createUser, createRole, createStatus, createTypeHistory, get_all_users, get_all_typeHistorique, get_all_status, get_all_roles

urlpatterns = [
    path('getUsers', get_all_users, name='get_all_users'),
    path('getRole/', get_all_roles, name='get_all_roles'),
    path('getType/', get_all_typeHistorique, name='get_all_typeHistorique'),
    path('getStatus/', get_all_status, name='get_all_status'),
    path('createUser/', createUser, name='create-user'),
    path('createRole/', createRole, name='create-role'),
    path('createStatus/', createStatus, name='create-status'),
    path('createTypeHistory/', createTypeHistory, name='create-type-history')
]