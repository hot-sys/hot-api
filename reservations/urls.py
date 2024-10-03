from django.urls import path
from .views import create_reservation, reservation_detail, reservation_list

urlpatterns = [
    path('create/', create_reservation, name='create_reservation'),
    path('<int:id>/', reservation_detail, name='reservation_detail'),
    path('all/', reservation_list, name='reservation_list'),
]
