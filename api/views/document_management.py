from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.text import slugify
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Document
from api.serializers import DocumentSerializer
from utils.helper import LogHelper


def generate_unique_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    count = 1
    while True:
        if not Document.objects.filter(slug=slug).exists():
            break
        slug = f"{base_slug}-{count}"
        count += 1
    return slug


def create_error_response(message, status_code):
    return Response(data={'message': message}, status=status_code)


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request_data = request.data
        if 'file' not in request_data:
            return Response(data={'message': 'Please upload a file valid file'})

        try:
            with transaction.atomic():
                slug = generate_unique_slug(request_data['title'])
                file_format = self.get_upload_file_format(request_data['file'])
                request_data['upload_by'] = request.user.id
                request_data['format'] = file_format
                request_data['slug'] = slug
                serializer = DocumentSerializer(data=request_data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            LogHelper.efail(e)
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            request_data = request.data.copy()  # Create a mutable copy
            with transaction.atomic():
                document = self.get_object()
                if 'title' in request_data:
                    if request_data['title'] != document.title:
                        slug = generate_unique_slug(request_data['title'])
                        request_data['slug'] = slug
                if 'file' in request_data:
                    file_format = self.get_upload_file_format(request_data['file'])
                    request_data['format'] = file_format
                    document.file.delete(save=False)
                    document.file = request_data['file']
                    document.save()

                serializer_data = DocumentSerializer(document, data=request_data, partial=True)
                if serializer_data.is_valid(raise_exception=True):
                    serializer_data.save()
                    return Response(data=serializer_data.data, status=status.HTTP_200_OK)
                else:
                    return Response(data=serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(data={'message': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            LogHelper.efail(e)
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        data = self.request
        if data.user.is_superuser:
            return Document.objects.all()
        else:
            return Document.objects.filter(upload_by__id=self.request.user.id)

    def get_upload_file_format(self, file):
        file_format = file.name.split('.')[1]
        return file_format
