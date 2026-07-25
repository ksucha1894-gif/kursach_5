from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from .models import User


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "username")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserRegisterAPIView(generics.CreateAPIView):
    """Контроллер для регистрации новых пользователей."""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []  # Регистрация доступна всем
