from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .pagination import CustomPagination
from .permissions import IsAuthor
from .serializer import (
    UserSerializer,
    IngredientSerializer,
    RecipesSerializer,
    TagSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    SubscribeSerializer,
)
from recipes.models import (
    Ingredient,
    Recipe,
    IngredientRecipe,
    Tag,
    Favorite,
    ShoppingCart,
)
from users.models import (
    User,
    Subscribe,
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
        permission_classes=[IsAuthor])
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
                Subscribe.objects.create(user=user, author=author)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            Subscribe,
            user=user,
            author=author,
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthor,)
    pagination_class = CustomPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (IsAuthor,)
    pagination_class = CustomPagination

    @staticmethod
    def send_message(ingredients):
        shopping_list = ''
        for ingredient in ingredients:
            shopping_list += (
                f"{ingredient['ingredient__name']}, "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}\n")
        file = 'shopping_list'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        return self.send_message(ingredients)

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[IsAuthor])
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
            # Проверяем валидность данных сериализатора
            if serializer.is_valid():
                # Если данные валидны, сохраняем экземпляр ShoppingCart
                serializer.save()
                # Возвращаем сериализованные данные и код состояния 201 CREATED
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            # Если данные невалидны, возвращаем ошибки валидации и код состояния 400 BAD REQUEST
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            ShoppingCart,
            user=request.user.id,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthor,)
    pagination_class = PageNumberPagination


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthor,)
    pagination_class = PageNumberPagination


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthor,)
    pagination_class = PageNumberPagination
