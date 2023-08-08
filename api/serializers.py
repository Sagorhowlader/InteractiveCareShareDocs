import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from authentication.models import CustomUser
from .models import Document, DocumentShare


def validate_email(email):
    pattern = r'[a-zA-Z][a-zA-Z0-9._]+@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise serializers.ValidationError('Please enter a valid email address')
    if CustomUser.objects.filter(email=email).exists():
        raise serializers.ValidationError("Email already exists")


def validate_password(password):
    if len(password) < 8:
        raise serializers.ValidationError('Password must have 8 characters')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, validators=[validate_email])
    first_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, validators=[validate_password])

    def create(self, validated_data):
        user_data = validated_data
        password = validated_data.get('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Password doesn't match"})
        user_data['password'] = make_password(password=user_data['password'])
        user = CustomUser.objects.create(**user_data)
        return user

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'is_admin': True if instance.is_staff else False,
            'is_superuser': instance.is_superuser,
            'is_active': instance.is_active,
            'create_at': instance.create_at
        }
        return data

    class Meta:
        model = CustomUser
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def to_representation(self, instance):
        data = super(DocumentSerializer, self).to_representation(instance)
        data['upload_by'] = f'{instance.upload_by.first_name} {instance.upload_by.last_name}'
        data['upload_details'] = {
            'id': instance.upload_by.id,
            'first_name': instance.upload_by.first_name,
            'last_name': instance.upload_by.last_name,
            'email': instance.upload_by.email
        }
        return data


class DocumentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentShare
        fields = '__all__'

    def to_representation(self, instance):
        share_by_data = UserSerializer(instance.share_by).data
        share_to_data = UserSerializer(instance.share_to).data
        document_data = DocumentSerializer(instance.document).data

        result_data = {
            'id': instance.id,
            'share_by': share_by_data,
            'share_to': share_to_data,
            'document': document_data,
            'sent_date': instance.sent_date,
        }

        return result_data
