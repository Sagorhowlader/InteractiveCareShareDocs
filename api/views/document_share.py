from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Document, DocumentShare
from api.serializers import DocumentShareSerializer
from authentication.models import CustomUser
from utils.helper import LogHelper


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def document_share_view(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                request_data = request.data
                if 'document' not in request_data:
                    return Response(data={'message': 'Document are missing'}, status=status.HTTP_400_BAD_REQUEST)
                if 'share_to' not in request_data:
                    return Response(data={'message': 'Select a user where you share documents'},
                                    status=status.HTTP_400_BAD_REQUEST)
                document = request_data['document']
                share_to = request_data['share_to']
                try:
                    request_data['document'] = Document.objects.get(pk=document, upload_by=request.user).pk
                except Document.DoesNotExist:
                    return Response(data={'message': 'Document not found or you do not have permission to share it.'},
                                    status=status.HTTP_404_NOT_FOUND)

                try:
                    request_data['share_to'] = CustomUser.objects.get(pk=share_to).pk
                except CustomUser.DoesNotExist:
                    return Response(data={'message': 'Sent user not found.'},
                                    status=status.HTTP_404_NOT_FOUND)

                request_data['share_by'] = request.user.id
                serializer_data = DocumentShareSerializer(data=request_data)
                if serializer_data.is_valid(raise_exception=True):
                    serializer_data.save()
                    return Response(data=serializer_data.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(data=serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            LogHelper.efail(e)
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_list_by_user(request):
    try:
        document_list = DocumentShare.objects.filter(share_by=request.user)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_documents = paginator.paginate_queryset(document_list, request)

        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': []
        }

        for document in paginated_documents:
            data = {
                'id': document.id,
                'sent_to': {
                    'id': document.share_to.id,
                    'first_name': document.share_to.first_name,
                    'last_name': document.share_to.last_name,
                    'email': document.share_to.email
                },
                'document': {
                    "id": document.document.id,
                    "title": document.document.title,
                    "slug": document.document.slug,
                    "description": document.document.description,
                    "format": document.document.format,
                    "file": document.document.file.url,
                    "upload_date": document.document.upload_date,
                    "update_date": document.document.update_date,
                },
                'sent_date': document.sent_date
            }
            response_data['results'].append(data)

        return Response(data=response_data)
    except Exception as e:
        LogHelper.efail(e)
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
