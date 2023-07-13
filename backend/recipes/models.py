from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User

MAX_LEN_SHORT = 7
MAX_LEN_MED = 50


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LEN_MED,
        verbose_name='Ingredient',
    )

    measurement_unit = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name='Measurement unit',
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self) -> str:
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LEN_MED,
        verbose_name='Tag',
        unique=True,
    )
    color = ColorField(default='#FF0000')
    slug = models.SlugField(
        max_length=MAX_LEN_MED,
        verbose_name='Slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'{self.slug}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Recipe author',
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=MAX_LEN_MED,
        verbose_name='Recipe name',
    )
    image = models.ImageField(
        verbose_name='Recipe image',
        upload_to='static/recipe/',
    )
    text = models.TextField(
        verbose_name='Recipe description',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time',
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'{self.name}'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe',
        on_delete=models.CASCADE,
        related_name='ingredient_list',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ingredient',
        on_delete=models.CASCADE,
        related_name='ingredient_list',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Amount',
        help_text='Enter the amount of ingredient',
        validators=[
            MinValueValidator(
                1,
                message='Enter a quantity greater than or equal to 1'
            ),
        ],
    )

    class Meta:
        verbose_name = 'Ingredient in the recipe'
        verbose_name_plural = 'Recipe Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe',
            )
        ]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class FavoriteAndShopModel(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Favorite(FavoriteAndShopModel):
    class Meta(FavoriteAndShopModel.Meta):
        verbose_name = 'Favorite Recipe'
        verbose_name_plural = 'Favorite Recipes'
        default_related_name = 'favorite'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            )
        ]


class ShoppingCart(FavoriteAndShopModel):
    class Meta(FavoriteAndShopModel.Meta):
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts'
        default_related_name = 'shopping_cart'
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'user',),
                name='unique_shopping_cart',
            ),
        )
