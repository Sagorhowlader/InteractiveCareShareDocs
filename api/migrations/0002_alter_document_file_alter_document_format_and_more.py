# Generated by Django 4.2.4 on 2023-08-06 12:52

import api.models
from django.conf import settings
import django.core.files.storage
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="file",
            field=models.FileField(
                storage=django.core.files.storage.FileSystemStorage(),
                upload_to="documents/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=[
                            "pdf",
                            "docx",
                            "txt",
                            "csv",
                            "xlsx",
                            "html",
                            "jpeg",
                            "png",
                            "jpg",
                            "ppt",
                        ]
                    ),
                    api.models.validate_file_size,
                ],
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="format",
            field=models.CharField(
                choices=[
                    ("pdf", "PDF"),
                    ("docx", "DOCX"),
                    ("ppt", "PPT"),
                    ("txt", "TXT"),
                    ("csv", "CSV"),
                    ("xlsx", "XLSX"),
                    ("html", "HTML"),
                    ("jpeg", "JPEG"),
                    ("jpg", "JPG"),
                    ("png", "PNG"),
                ],
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="title",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name="DocumentShare",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sent_date", models.DateTimeField(auto_now_add=True)),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.document"
                    ),
                ),
                (
                    "share_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shared_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "share_to",
                    models.ManyToManyField(
                        related_name="shared_to", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "Document Share",
                "verbose_name_plural": "Document Shares",
                "db_table": "document_share",
            },
        ),
    ]