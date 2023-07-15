from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscribe, User
from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthor
from .serializer import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipesSerializer,
    TagSerializer,
    ShoppingCartSerializer,
    SubscribeSerializer,
    UserSerializer,
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        serializer = SubscribeSerializer(
            author,
            data=request.data,
            context={'request': request}
        )
        if request.method == 'POST':
            if serializer.is_valid():
                Subscribe.objects.create(
                    user=user, author=author
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        get_object_or_404(
            Subscribe,
            user=user,
            author=author,
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = (IsAuthor,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesSerializer
        return RecipeCreateSerializer

    @staticmethod
    def generate_shopping_list(ingredients):
        shopping_list = []
        for ingredient in ingredients:
            shopping_line = (
                f"{ingredient['ingredient__name']}: "
                f"{ingredient['total']} "
                f"{ingredient['ingredient__measurement_unit']}\n"
            )
            shopping_list.append(shopping_line)
        return "".join(shopping_list)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total=Sum('amount'))
        shopping_list = self.generate_shopping_list(ingredients)
        response = HttpResponse(
            shopping_list, content_type="text/plain; charset=utf-8"
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response

    def handle_favorite_or_shoping_cart(
        self, request, pk, serializer_class, model_class
    ):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        recipe = self.get_object()
        serializer = serializer_class(data=data, context={'request': request})

        if request.method == 'POST':
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        get_object_or_404(
            model_class,
            user=request.user.id,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.handle_favorite_or_shoping_cart(
            request, pk, ShoppingCartSerializer, ShoppingCart
        )

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.handle_favorite_or_shoping_cart(
            request, pk, FavoriteSerializer, Favorite
        )


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthor,)
    pagination_class = CustomPagination


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthor,)
    pagination_class = CustomPagination
