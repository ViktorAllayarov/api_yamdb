from rest_framework import serializers

from users.models import User


class AuthSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ("email", "username",)
        model = User

    def validate(self, data):
        if User.objects.filter(username=data.get("username")).exists():
            raise serializers.ValidationError('Пользователь с таким username уже существует.')
        if User.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует.')
        return data