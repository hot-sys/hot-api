from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserViewSet, UserPreferenceViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'preferences', UserPreferenceViewSet)

urlpatterns = router.urls
