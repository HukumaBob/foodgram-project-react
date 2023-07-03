from django.urls import include, path
from rest_framework import routers
from .views import (
    UserViewSet,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
)

app_name = 'api'

# Create a router for API endpoints
router_v1 = routers.DefaultRouter()

# Register viewsets for different models
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
