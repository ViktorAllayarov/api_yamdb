from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status, views, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAnonymous
from .serializers import (
    AuthSignupSerializer,
    GetJWTTokenSerializer,
    UserViewSerializer,
)
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status, views, mixins, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAnonymous, IsAuthorReadOnly
from .serializers import (
    AuthSignupSerializer,
    GetJWTTokenSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,)
from users.models import User
from reviews.models import Category, Title, Genre

EMAIL_TITLE = "Приветствуем {}"
EMAIL_MESSAGE = "Ваш секретный код: {}"


class MyMixinsSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    pass


class CategoryViewSet(MyMixinsSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(MyMixinsSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorReadOnly, )
    pagination_class = PageNumberPagination


class GenreViewSet(MyMixinsSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthorReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


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
    pagination_class = LimitOffsetPagination
    lookup_field = "username"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        # если пользователь admin, то можно менять поле role,
        # в остальных случаях нелья
        if request.user.role == RoleChoices.ADMIN or request.user.is_staff:
            serializer.save()
        else:
            serializer.save(role=self.request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
