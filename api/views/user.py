from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.serializers import UserSerializer
from authentication.models import CustomUser
from utils.permission import UserOwnerPermission


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        if 'is_superuser' in request.data or 'is_staff' in request.data:
            if request.user != IsAdminUser:
                return Response(data={'message': 'You have no permission to create admin user'},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            if 'is_superuser' in request.data or 'is_staff' in request.data:
                if request.user != IsAdminUser:
                    return Response(data={'message': 'You have no permission to update admin user'},
                                    status=status.HTTP_400_BAD_REQUEST)

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
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'partial_update':
            permission_classes = [UserOwnerPermission]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
