from django.http import FileResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Document, DocumentShare
from utils.helper import LogHelper


class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)

            # Check if the user is a superuser or the document's uploader
            if request.user.is_superuser or document.upload_by == request.user:
                response = FileResponse(document.file, as_attachment=True)
                return response

            # Check if the user has shared the document and has permission to download
            document_share = DocumentShare.objects.filter(document=document, share_to=request.user).first()
            if document_share:
                response = FileResponse(document.file, as_attachment=True)
                return response

            return Response(
                data={'message': 'You do not have permission to download this file or Document are not share with You'},
                status=status.HTTP_403_FORBIDDEN
            )

        except Document.DoesNotExist:
            return Response(
                data={'message': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            LogHelper.efail(e)
            return Response(
                data={'message': 'An error occurred'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
