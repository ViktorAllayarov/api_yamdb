from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, status, views, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAnonymous, IsAdminOrReadOnly
from .serializers import AuthSignupSerializer, GetJWTTokenSerializer, UserViewSerializer
from users.models import User

EMAIL_TITLE = "Приветствуем {}"
EMAIL_MESSAGE = "Ваш секретный код: {}"


class AuthSignupView(views.APIView):
    """Класс для регистрации новых пользователей."""

    permission_classes = (IsAnonymous,)

    def post(self, request):
        serializer = AuthSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            serializer.data.get("username"),
            email=serializer.data.get("email"),
        )
        send_mail(
            EMAIL_TITLE.format(serializer.data.get("username")),
            EMAIL_MESSAGE.format(user.password),
            settings.ADMINS_EMAIL,
            [serializer.data.get("email")],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetJWTTokenView(views.APIView):
    """
    Класс для получения JWT токена в обмен
    на username и confirmation code.
    """

    permission_classes = (IsAnonymous,)

    def post(self, request):
        serializer = GetJWTTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, password=serializer.data.get("confirmation_code")
        )
        refresh = RefreshToken.for_user(user)

        return Response(
            {"token": str(refresh.access_token)},
            status=status.HTTP_201_CREATED,
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer
    permission_classes = (permissions.IsAdminUser,)
