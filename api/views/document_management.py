from rest_framework import status, viewsets
from rest_framework.response import Response

from api.models import Document
from api.serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = request.user.id
        data['upload_by'] = user_id
        file_input = data['file'].content_type
        input_input = data['format']
        if self.check_upload_file_format(file_input, input_input):
            return Response(
                data={
                    'message': 'You input wrong format of file.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_upload_file_format(self, file_format, input_format):
        file_format_dic = {
            "text/plain": "txt",
            "application/pdf": "pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            "image/jpeg": "jpeg",
            "application/vnd.ms-powerpoint": "ppt",
            "text/csv": "csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
            "image/png": "png",
            "text/html": "html"

        }

        if file_format_dic[file_format] != input_format:
            return True
        return False
