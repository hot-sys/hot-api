"""hotel_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic.base import RedirectView

def custom_404_view(request, exception=None):
    return RedirectView.as_view(url='/docs/api/', permanent=False)(request)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/api/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='users-swagger-ui'),
    path('docs/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/users/', include('hot_users.urls')),
    path('api/history/', include('hot_history.urls')),
    path('api/rooms/', include('hot_rooms.urls')),
    path('api/services/', include('hot_services.urls')),
    path('api/clients/', include('hot_clients.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', RedirectView.as_view(url='/docs/api/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_404_view
urlpatterns += [
    re_path(r'^.*$', custom_404_view),
]