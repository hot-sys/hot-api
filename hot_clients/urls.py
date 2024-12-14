from django.urls import path
from .views import all, get_by_id, create, update, search, delete, recover

urlpatterns = [
    path('create', create, name='create'),
    path('all', all, name='all'),
    path('search', search, name='search'),
    path('get/<int:idClient>', get_by_id, name='get_by_id'),
    path('update/<int:idClient>', update, name='update'),
    path('delete/<int:idClient>', delete, name='delete'),
    path('recover/<int:idClient>', recover, name='recover'),
]