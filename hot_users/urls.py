from django.urls import path
from .views import create, update_current_user, update_admin_user, update_poste, delete_user, recover_user, create_role, login, current_user, get_role, get_all_roles, get_all_users, get_user


urlpatterns = [
    path('login/', login, name='login'),
    path('current/', current_user, name='current_user'),
    path('create/', create, name='create'),
    path('update_current/', update_current_user, name='update_current_user'),
    path('update_admin/<int:idUser>', update_admin_user, name='update_admin_user'),
    path('update_poste/<int:idUser>', update_poste, name='update_poste'),
    path('delete/<int:idUser>', delete_user, name='delete_user'),
    path('recover/<int:idUser>', recover_user, name='recover_user'),
    path('list', get_all_users, name='get_all_users'),
    path('get/<int:idUser>', get_user, name='get_user'),
    path('role', get_all_roles, name='get_all_roles'),
    path('role/<int:idRole>', get_role, name='get_role'),
    path('createrole/', create_role, name='create_role'),
]