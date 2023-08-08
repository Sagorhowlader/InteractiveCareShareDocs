from rest_framework.permissions import BasePermission


class AdminPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class UserOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class DocumentOwnerOrAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the request user is an admin or the document owner
        return request.user.is_superuser or obj.upload_by == request.user

