from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    # create user
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email', ''),
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
                password=request.data.get('password')
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # user list (only for staff)
    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'دسترسی ندارید.'}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    # user details
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # update user
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in request.data:
                user.set_password(request.data['password'])
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete user
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if not request.user.is_staff and request.user != user:
            return Response({'detail': 'فقط مدیر یا خود کاربر می‌تواند حذف کند.'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # change password
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({'status': 'رمز عبور تغییر یافت'})
        return Response({'detail': 'رمز عبور معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)
