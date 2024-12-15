from django.urls import path
from .views import create_status, get_all_status, update_service, delete_service, recover_service, create_service, get_by_id_service, update_status, get_by_id_status, get_all_service

urlpatterns = [
    path('create', create_service, name='create_service'),
    path('all', get_all_service, name='get_all_service'),
    path('get/<int:idService>', get_by_id_service, name='get_by_id_service'),
    path('update/<int:idService>', update_service, name='update_service'),
    path('delete/<int:idService>', delete_service, name='delete_service'),
    path('recover/<int:idService>', recover_service, name='recover_service'),
    path('status/all', get_all_status, name='get_all_status'),
    path('status/create', create_status, name='create_status'),
    path('status/get/<int:idStatus>', get_by_id_status, name='get_by_id_status'),
    path('status/update/<int:idStatus>', update_status, name='update_status'),
]