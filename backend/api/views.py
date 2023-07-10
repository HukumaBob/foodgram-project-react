from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly)
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

# CustomUserViewSet handles user-related operations
class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination

    # Action to get user subscriptions
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

    # Action to handle user subscription to another user
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


# TagViewSet handles tag-related operations
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


# IngredientViewSet handles ingredient-related operations
class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_class = (IngredientFilter,)
    search_fields = ('^name',)


# RecipeViewSet handles recipe-related operations
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = (IsAuthor,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    # Determine the serializer class based on the request method
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesSerializer
        return RecipeCreateSerializer

    # Save the shopping list to a file
    @staticmethod
    def save_shopping_list(ingredients):
        with open('shopping_list.txt', 'w') as file:
            for ingredient in ingredients:
                shopping_line = (
                    f"{ingredient['ingredient__name']}: "
                    f"{ingredient['amount']} "
                    f"{ingredient['ingredient__measurement_unit']}\n"
                )
                file.write(shopping_line)
        return Response(
            {'message': 'Shopping list downloaded'},
            status=status.HTTP_200_OK
        )

    # Action to download the shopping cart as a file
    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        return self.save_shopping_list(ingredients)

    # Action to add or remove a recipe from the shopping cart
    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = ShoppingCartSerializer(
            data=data, context={'request': request}
        )
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
            ShoppingCart,
            user=request.user.id,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Action to add or remove a recipe from favorites
    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
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
            Favorite,
            user=request.user.id,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# FavoriteViewSet handles favorite-related operations
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthor,)
    pagination_class = CustomPagination


# ShoppingCartViewSet handles shopping cart-related operations
class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthor,)
    pagination_class = CustomPagination
