from rest_framework import serializers

from users.models import User


class AuthSignupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "email",
            "username",
        )
        model = User
