from django.urls import path
from rest_framework import routers

from api.views import document_download
from api.views import document_management
from api.views import document_share
from api.views import user

router = routers.DefaultRouter()
router.register(r'user', user.UserViewSet, basename='user')
router.register(r'document', document_management.DocumentViewSet, basename='document')
urlpatterns = [
    path('document-download/<int:pk>/', document_download.DownloadFileView.as_view(), name='document-download'),
    path('document-share/', document_share.document_share_view, name='document-share'),
    path('document-share-list-by-user/', document_share.document_share_list_by_user, name='document-share-list-by-user')
]
urlpatterns = urlpatterns + router.urls
