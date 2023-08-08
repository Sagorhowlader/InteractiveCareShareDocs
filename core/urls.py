from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from utils.swagger import schema_view

urlpatterns = [
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("admin/", admin.site.urls),
    path("auth/", include('authentication.urls')),
    path("api/", include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
