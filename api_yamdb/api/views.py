from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import status, views

from .serializers import AuthSignupSerializer
from users.models import User


class AuthSignupView(views.APIView):
    """Класс для регистрации новых пользователей."""

    def post(self, request):
        serializer = AuthSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            serializer.data.get('username'),
            email=serializer.data.get('email'),
        )
        send_mail(
            f'Приветствуем {serializer.data.get("username")}',
            f'Ваш секретный код: {user.password}',
            settings.ADMINS_EMAIL,
            [serializer.data.get("email")],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
