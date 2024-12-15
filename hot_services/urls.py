from django.urls import path
from .views import create_status, get_all_status, create_item_service, update_item_service, delete_item_service, recover_item_service, get_detail_item, get_all_service_item, update_service, delete_service, recover_service, create_service, get_by_id_service, update_status, get_by_id_status, get_all_service

urlpatterns = [
    path('create', create_service, name='create_service'),
    path('all', get_all_service, name='get_all_service'),
    path('get/<int:idService>', get_by_id_service, name='get_by_id_service'),
    path('update/<int:idService>', update_service, name='update_service'),
    path('delete/<int:idService>', delete_service, name='delete_service'),
    path('recover/<int:idService>', recover_service, name='recover_service'),
    path('item/create/<int:idService>', create_item_service, name='create_item_service'),
    path('item/delete/<int:idItem>', delete_item_service, name='delete_item_service'),
    path('item/recover/<int:idItem>', recover_item_service, name='recover_item_service'),
    path('item/all/<int:idService>', get_all_service_item, name='get_all_service_item'),
    path('item/detail/<int:idItem>', get_detail_item, name='get_detail_item'),
    path('item/update/<int:idItem>', update_item_service, name='update_item_service'),
    path('status/all', get_all_status, name='get_all_status'),
    path('status/create', create_status, name='create_status'),
    path('status/get/<int:idStatus>', get_by_id_status, name='get_by_id_status'),
    path('status/update/<int:idStatus>', update_status, name='update_status'),
]