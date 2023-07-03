from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAuthorOrModerator
from .serializer import (
    UserSerializer,
    IngredientSerializer,
    RecipesSerializer,
    TagSerializer,
)
from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
)
from users.models import User


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthorOrModerator,)
    pagination_class = PageNumberPagination


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthorOrModerator,)
    pagination_class = PageNumberPagination

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (IsAuthorOrModerator,)
    pagination_class = PageNumberPagination

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthorOrModerator,)
    pagination_class = PageNumberPagination