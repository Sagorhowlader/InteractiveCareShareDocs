from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="InteractiveCareShareDocs API",
        default_version='v1.0.0',
        description="InteractiveCareShareDocs Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
