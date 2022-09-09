# from django.contrib import admin
# from django.contrib.auth import get_user_model

# User = get_user_model()


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'username', 'email', 'first_name', 'last_name', 'date_joined',
#     )
#     search_fields = ('email', 'username', 'first_name', 'last_name')
#     list_filter = ('date_joined', 'email', 'first_name')
#     empty_value_display = '-пусто-'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username')
    list_filter = ('email', 'username')


@admin.register(User)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
