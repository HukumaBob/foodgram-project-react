from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.fields import SerializerMethodField
from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
)
from users.models import User
from rest_framework import serializers


class UserSerializer(UserSerializer):
    # Serializer for User model

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            print(user)
            return False
        return user.subscriber.exists(author_id=obj.pk)


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)

class RecipesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
