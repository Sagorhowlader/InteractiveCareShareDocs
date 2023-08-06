from rest_framework import routers

from api.views import user

router = routers.DefaultRouter()
router.register(r'user', user.UserViewSet, basename='user')

urlpatterns = router.urls
