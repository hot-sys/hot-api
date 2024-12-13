from django.urls import path
from .views import all, get_room, create, update_by_admin, delete_by_admin, recover_by_admin

urlpatterns = [
    path('all', all, name='all'),
    path('create', create, name='create'),
    path('get/<int:idRoom>', get_room, name='getRoom'),
    path('update/<int:idRoom>', update_by_admin, name='update'),
    path('delete/<int:idRoom>', delete_by_admin, name='delete'),
    path('recover/<int:idRoom>', recover_by_admin, name='recover'),
]