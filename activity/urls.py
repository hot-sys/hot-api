from django.urls import path
from .views import create_activity, activity_detail, activity_list, type_activity_list

urlpatterns = [
    path('create/', create_activity, name='create_activity'),
    path('<int:id>/', activity_detail, name='activity_detail'),
    path('all/', activity_list, name='activity_list'),
    path('types/', type_activity_list, name='type_activity_list'),
]
