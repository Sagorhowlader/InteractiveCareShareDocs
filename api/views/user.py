from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import UserSerializer
from authentication.models import CustomUser


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
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
