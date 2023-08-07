from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Document


class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            if request.user.is_staff:
                document = get_object_or_404(Document, pk=pk)
            else:
                document = get_object_or_404(Document, pk=pk, upload_by=request.user)
            response = FileResponse(document.file, as_attachment=True)
            return response
        except Exception:
            return Response(data={'message': 'Document not found or You are not permission to download this file'},
                            status=status.HTTP_404_NOT_FOUND)
