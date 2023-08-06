from rest_framework import routers

from api.views import document_management
from api.views import user

router = routers.DefaultRouter()
router.register(r'user', user.UserViewSet, basename='user')
router.register(r'document', document_management.DocumentViewSet, basename='document')
urlpatterns = router.urls
