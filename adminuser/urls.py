from django.urls import path
from .views import register, login, user_detail, user_list

urlpatterns = [
    path('register/', register, name='admin_register'),
    path('login/', login, name='admin_login'),
    path('<int:id>/', user_detail, name='admin_user_detail'),
    path('all/', user_list, name='admin_user_list'),
]
