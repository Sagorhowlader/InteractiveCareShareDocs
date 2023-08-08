import oauth2_provider.views as oauth2_views
from django.urls import path, include

app_name = 'authentication'
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]
urlpatterns = [
    path("o/", include('oauth2_provider.urls', namespace='oauth2_provider')),
]
