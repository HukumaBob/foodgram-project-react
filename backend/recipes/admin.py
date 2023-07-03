from django.contrib import admin

from .models import (Recipe,
                     IngredientRecipe,
                     Ingredient,
                     Tag,
                     ShoppingCart
                     )


class IngredientInline(admin.StackedInline):
    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
    )
    inlines = [IngredientInline]
    list_editable = ('name',)
    list_filter = ('author', 'name', 'tags',)
    search_fields = ('author', 'name',)
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'slug',
        'color',
    )
    list_editable = ('slug',)
    list_filter = ('name', 'slug',)
    search_fields = ('name', 'slug')

@admin.register(ShoppingCart)
class ShoppingCart(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_filter = ('recipe',)
    search_fields = ('recipe',)