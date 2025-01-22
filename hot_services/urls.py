from django.urls import path
from .views import create_status, stat, get_all_status, get_all_commande_client, get_all_commande_client_wp, create_commande_client, confirmeCommande, confirmeNotReceivedCommande, search_item_service, get_image_item_service, create_image_item_service, delete_image_item_service, filter_commande, simulate, create_item_service, create_commande, get_commande_item, get_all_commande, update_item_service, delete_item_service, recover_item_service, get_detail_item, get_all_service_item, update_service, delete_service, recover_service, create_service, get_by_id_service, update_status, get_by_id_status, get_all_service

urlpatterns = [
    path('stat', stat, name='stat'),
    path('create', create_service, name='create_service'),
    path('all', get_all_service, name='get_all_service'),
    path('get/<int:idService>', get_by_id_service, name='get_by_id_service'),
    path('update/<int:idService>', update_service, name='update_service'),
    path('delete/<int:idService>', delete_service, name='delete_service'),
    path('recover/<int:idService>', recover_service, name='recover_service'),

    path('commande/create', create_commande, name='create_commande'),
    path('commande/create-client', create_commande_client, name='create_commande_client'),
    path('commande/filter', filter_commande, name='filter_commande'),
    path('commande/simulate', simulate, name='simulate'),
    path('commande/all', get_all_commande, name='get_all_commande'),
    path('commande/all-client/<int:idClient>', get_all_commande_client, name='get_all_commande_client'),
    path('commande/all-client-wp/<int:idClient>', get_all_commande_client_wp, name='get_all_commande_client_wp'),
    path('commande/get/<int:idCommande>', get_commande_item, name='get_commande_item'),
    path('commande/confirme/<int:idCommande>', confirmeCommande, name='confirmeCommande'),
    path('commande/confirme-no-received/<int:idCommande>', confirmeNotReceivedCommande, name='confirmeNotReceivedCommande'),

    path('item/search/<int:idService>', search_item_service, name='search_item_service'),
    path('item/create/<int:idService>', create_item_service, name='create_item_service'),
    path('item/delete/<int:idItem>', delete_item_service, name='delete_item_service'),
    path('item/recover/<int:idItem>', recover_item_service, name='recover_item_service'),
    path('item/all/<int:idService>', get_all_service_item, name='get_all_service_item'),
    path('item/detail/<int:idItem>', get_detail_item, name='get_detail_item'),
    path('item/update/<int:idItem>', update_item_service, name='update_item_service'),
    path('item/createimage/<int:idItem>', create_image_item_service, name='create_image_item_service'),
    path('item/deleteimage/<int:idImage>', delete_image_item_service, name='delete_image_item_service'),
    path('item/image/<int:idItem>', get_image_item_service, name='get_image_item_service'),

    path('status/all', get_all_status, name='get_all_status'),
    path('status/create', create_status, name='create_status'),
    path('status/get/<int:idStatus>', get_by_id_status, name='get_by_id_status'),
    path('status/update/<int:idStatus>', update_status, name='update_status'),
]