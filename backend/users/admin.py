from django.contrib import admin
from .models import User, Subscribe


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_editable = ('email',)
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = '-empty-'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',)
    search_fields = (
        'user__email',
        'author__email',)
    empty_value_display = '-empty-'
