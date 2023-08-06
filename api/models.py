from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models

from authentication.models import CustomUser

# Create your models here.
FORMAT_CHOICE = (
    ('pdf', 'PDF'),
    ('docx', 'DOCX'),
    ('ppt', 'PPT'),
    ('txt', 'TXT'),
    ('csv', 'CSV'),
    ('xlsx', 'XLSX'),
    ('html', 'HTML'),
    ('jpeg', 'JPEG'),
    ('jpg', 'JPG'),
    ('png', 'PNG'),
)


def validate_file_size(value):
    filesize = value.size

    if filesize > 2 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 2MB")
    else:
        return value


class Document(models.Model):
    upload_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.TextField(null=True)
    format = models.CharField(choices=FORMAT_CHOICE, max_length=5, blank=False)
    file = models.FileField(
        null=False,
        upload_to='documents/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'docx', 'txt', 'csv', 'xlsx', 'html', 'jpeg', 'png', 'jpg', 'ppt']),
            validate_file_size
        ],
        storage=FileSystemStorage(),

    )
    upload_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        db_table = "Document"

    def __str__(self):
        return self.title


class DocumentShare(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    share_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shared_by')
    share_to = models.ManyToManyField(CustomUser, related_name='shared_to')

    sent_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Document Share"
        verbose_name_plural = "Document Shares"
        db_table = "document_share"
