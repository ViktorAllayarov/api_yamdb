from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from rest_framework import status, views, mixins, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAnonymous, IsAuthorReadOnly, IsAdmin, IsAdminOrReadOnly, AuthorPlusOrReadOnly
from .serializers import (
    AuthSignupSerializer,
    GetJWTTokenSerializer,
    TitleSerializer,
    GenreSerializer,
    UserViewSerializer,
    CategorySerializer,
    ReviewSerializer,
    CommentSerializer
)
from users.models import RoleChoices, User
from reviews.models import Category, Title, Genre, Review, Comment

EMAIL_TITLE = "Приветствуем {}"
EMAIL_MESSAGE = "Ваш секретный код: {}"


class MyMixinsSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    pass


class CategoryViewSet(MyMixinsSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(MyMixinsSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorReadOnly,)
    pagination_class = PageNumberPagination


class GenreViewSet(MyMixinsSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class AuthSignupView(views.APIView):
    """Класс для регистрации новых пользователей."""

    def post(self, request):
        username_and_email_exists = User.objects.filter(
            username=request.data.get("username"),
            email=request.data.get("email"),
        ).exists()
        if username_and_email_exists:
            return Response(request.data, status=status.HTTP_200_OK)
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

        return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"

    def update(self, request, *args, **kwargs):
        if request.method in ("PUT"):
            return Response(
                request.data, status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    ermission_classes = (AuthorPlusOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("review",)
    lookup_field = "review"

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return self.get_title().comments.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    ermission_classes = (AuthorPlusOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("comment",)
    lookup_field = "comment"

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()
