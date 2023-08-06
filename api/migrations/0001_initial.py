# Generated by Django 4.2.4 on 2023-08-06 11:48

import api.models
from django.conf import settings
import django.core.files.storage
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(null=True)),
                (
                    "format",
                    models.CharField(
                        choices=[
                            ("pdf", "PDF"),
                            ("docx", "DOCX"),
                            ("txt", "TXT"),
                            ("csv", "CSV"),
                            ("xlsx", "XLSX"),
                            ("html", "HTML"),
                            ("jpeg", "JPEG"),
                            ("png", "PNG"),
                        ],
                        max_length=5,
                    ),
                ),
                (
                    "file",
                    models.FileField(
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
                                ]
                            ),
                            api.models.validate_file_size,
                        ],
                    ),
                ),
                ("upload_date", models.DateField(auto_now_add=True)),
                ("update_date", models.DateField(auto_now=True)),
                (
                    "upload_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Document",
                "verbose_name_plural": "Documents",
                "db_table": "Document",
            },
        ),
    ]