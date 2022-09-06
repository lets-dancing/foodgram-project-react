# from django.contrib import admin

# from .models import (FavoriteRecipe, Ingredient, Recipe, IngredientInRecipe,
#                      ShoppingCart, Subscribe, Tag)


# class RecipeIngredientAdmin(admin.StackedInline):
#     model = IngredientInRecipe
#     autocomplete_fields = ('ingredient',)
#     extra = 1
#     min_num = 1


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):

#     list_display = (
#         'id', 'get_author', 'name', 'text',
#         'cooking_time', 'get_tags', 'get_ingredients',
#         'get_favorite_count')
#     search_fields = ('name', 'cooking_time', 'author__email',
#                      'ingredients__name')
#     list_filter = ('tags',)
#     inlines = (RecipeIngredientAdmin,)
#     empty_value_display = '-пусто-'

#     @admin.display(description='author email')
#     def get_author(self, obj):
#         return obj.author.email

#     @admin.display(description='tags')
#     def get_tags(self, obj):
#         return ', '.join([i.name for i in obj.tags.all()])

#     @admin.display(description='ingredient')
#     def get_ingredients(self, obj):
#         return '\n '.join([
#             f'{item["ingredient__name"]} - {item["amount"]}'
#             f' {item["ingredient__measurement_unit"]}.'
#             for item in obj.recipe.values(
#                 'ingredient__name',
#                 'amount', 'ingredient__measurement_unit')])

#     @admin.display(description='favorite count')
#     def get_favorite_count(self, obj):
#         return obj.favorite_recipe.count()


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):

#     list_display = ('id', 'name', 'color', 'slug')
#     search_fields = ('name', 'slug')
#     empty_value_display = '-пусто-'


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):

#     list_display = ('id', 'name', 'measurement_unit',)
#     search_fields = ('name', 'measurement_unit')
#     empty_value_display = '-пусто-'


# @admin.register(Subscribe)
# class SubscribeAdmin(admin.ModelAdmin):

#     list_display = ('id', 'user', 'author', 'created',)
#     search_fields = ('user__email', 'author__email',)
#     empty_value_display = '-пусто-'


# @admin.register(FavoriteRecipe)
# class FavoriteRecipeAdmin(admin.ModelAdmin):

#     list_display = ('id', 'user', 'get_recipe', 'get_count')
#     empty_value_display = '-пусто-'

#     @admin.display(description='recipes')
#     def get_recipe(self, obj):
#         return [
#             f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

#     @admin.display(description='count')
#     def get_count(self, obj):
#         return obj.recipe.count()


# @admin.register(ShoppingCart)
# class SoppingCartAdmin(admin.ModelAdmin):

#     list_display = ('id', 'user', 'get_recipe', 'get_count')
#     empty_value_display = '-пусто-'

#     @admin.display(description='recipes')
#     def get_recipe(self, obj):
#         return [
#             f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

#     @admin.display(description='count')
#     def get_count(self, obj):
#         return obj.recipe.count()

from django.contrib import admin

from .models import (
    FavoriteRecipe, Ingredient, IngredientInRecipe, Recipe, ShoppingCart, Tag,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('count_favorites',)

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = 'Добавлено в избранное'


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass
