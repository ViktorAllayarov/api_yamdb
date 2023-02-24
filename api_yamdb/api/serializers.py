from rest_framework import serializers
from rest_framework.exceptions import NotFound

from users.models import User
from reviews.models import Category, Title, Genre, Review, Comment


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class AuthSignupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "email",
            "username",
        )
        model = User

    def validate(self, data):
        if data.get("username") == "me":
            raise serializers.ValidationError("Ошибка: недопустимое имя")
        return data


class GetJWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        if not User.objects.filter(username=data.get("username")).exists():
            raise NotFound("Ошибка: не верный username")
        if not User.objects.filter(username=data.get("username")).exists():
            raise NotFound("Ошибка: не верный username")
        if not User.objects.filter(
            password=data.get("confirmation_code")
        ).exists():
            raise serializers.ValidationError(
                "Ошибка: не верный confirmation_code"
            )
        return data


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class ReviewSerializer(serializers.Serializer):
    class Meta:
        model = Review
        fields = "__all__"


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = "__all__"
