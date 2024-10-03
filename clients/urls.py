from django.urls import path
from .views import register, login, user_detail, user_list, activate_account, logout

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<str:email>', activate_account, name='activate_account'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('detail/', user_detail, name='user_detail'),
    path('all/', user_list, name='user_list'),
]
