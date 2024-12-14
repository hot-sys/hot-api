from django.urls import path
from .views import all, get_room, imageall, delete_image, image_room, createimage, create, update_by_admin, delete_by_admin, recover_by_admin, upload

urlpatterns = [
    path('all', all, name='all'),
    path('create', create, name='create'),
    path('upload', upload, name='upload'),
    path('createimage/<int:idRoom>', createimage, name='createimage'),
    path('imageall', imageall, name='imageall'),
    path('image/<int:idRoom>', image_room, name='image'),
    path('deleteimage/<int:idImage>', delete_image, name='delete_image'),
    path('get/<int:idRoom>', get_room, name='getRoom'),
    path('update/<int:idRoom>', update_by_admin, name='update'),
    path('delete/<int:idRoom>', delete_by_admin, name='delete'),
    path('recover/<int:idRoom>', recover_by_admin, name='recover'),
]