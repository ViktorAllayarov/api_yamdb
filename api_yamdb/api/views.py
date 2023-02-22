from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, views

from .serializers import AuthSignupSerializer
from users.models import User

EMAIL_TITLE = 'Приветствуем {}'
EMAIL_MESSAGE = 'Ваш секретный код: {}'

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
            EMAIL_TITLE.format(serializer.data.get("username")),
            EMAIL_MESSAGE.format(user.password),
            settings.ADMINS_EMAIL,
            [serializer.data.get("email")],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)