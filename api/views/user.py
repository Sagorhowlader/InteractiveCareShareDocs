from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers import UserSerializer
from authentication.models import CustomUser


class AdminPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            if 'is_superuser' in request.data:
                user.is_superuser = True
                user.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(pk=kwargs['pk'])
            if 'password' in request.data and request.data['password'] == user.password:
                return Response(data={'message': 'Error! You have entered a previously used password'},
                                status=status.HTTP_400_BAD_REQUEST)

            if 'email' in request.data and request.data['email'] == user.email:
                return Response(data={'message': 'Error! You have entered a previously used email'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                if getattr(user, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    user._prefetched_objects_cache = {}
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'destroy':
            print("trigger")
            permission_classes = [AdminPermissions]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
