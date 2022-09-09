# import django.contrib.auth.password_validation as validators
# from django.contrib.auth import authenticate, get_user_model
# from django.contrib.auth.hashers import make_password
# from django.db.models import F
# from django.shortcuts import get_object_or_404
# from drf_base64.fields import Base64ImageField
# from recipes.models import Ingredient, Recipe, RecipeIngredient, Subscribe, Tag
# from rest_framework import serializers

# User = get_user_model()
# ERR_MSG = 'Не удается войти в систему с предоставленными учетными данными.'


# class TokenSerializer(serializers.Serializer):
#     email = serializers.CharField(
#         label='Email',
#         write_only=True)
#     password = serializers.CharField(
#         label='Пароль',
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         write_only=True)
#     token = serializers.CharField(
#         label='Токен',
#         read_only=True)

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         if email and password:
#             user = authenticate(
#                 request=self.context.get('request'),
#                 email=email,
#                 password=password)
#             if not user:
#                 raise serializers.ValidationError(
#                     ERR_MSG,
#                     code='authorization')
#         else:
#             msg = 'Необходимо указать "адрес электронной почты" и "пароль".'
#             raise serializers.ValidationError(
#                 msg,
#                 code='authorization')
#         attrs['user'] = user
#         return attrs


# class GetIsSubscribedMixin:

#     def get_is_subscribed(self, obj):
#         user = self.context['request'].user
#         if not user.is_authenticated:
#             return False
#         return user.follower.filter(author=obj).exists()


# class UserListSerializer(
#         GetIsSubscribedMixin,
#         serializers.ModelSerializer):
#     is_subscribed = serializers.BooleanField(read_only=True)

#     class Meta:
#         model = User
#         fields = (
#             'email', 'id', 'username',
#             'first_name', 'last_name', 'is_subscribed')


# class UserCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             'id', 'email', 'username',
#             'first_name', 'last_name', 'password',)

#     def validate_password(self, password):
#         validators.validate_password(password)
#         return password


# class UserPasswordSerializer(serializers.Serializer):
#     new_password = serializers.CharField(
#         label='Новый пароль')
#     current_password = serializers.CharField(
#         label='Текущий пароль')

#     def validate_current_password(self, current_password):
#         user = self.context['request'].user
#         if not authenticate(
#                 username=user.email,
#                 password=current_password):
#             raise serializers.ValidationError(
#                 ERR_MSG, code='authorization')
#         return current_password

#     def validate_new_password(self, new_password):
#         validators.validate_password(new_password)
#         return new_password

#     def create(self, validated_data):
#         user = self.context['request'].user
#         password = make_password(
#             validated_data.get('new_password'))
#         user.password = password
#         user.save()
#         return validated_data


# class TagSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Tag
#         fields = (
#             'id', 'name', 'color', 'slug',)


# class IngredientSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Ingredient
#         fields = '__all__'


# class RecipeIngredientSerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(
#         source='ingredient.id')
#     name = serializers.ReadOnlyField(
#         source='ingredient.name')
#     measurement_unit = serializers.ReadOnlyField(
#         source='ingredient.measurement_unit')

#     class Meta:
#         model = RecipeIngredient
#         fields = (
#             'id', 'name', 'measurement_unit', 'amount')


# class RecipeUserSerializer(GetIsSubscribedMixin, serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField(
#         read_only=True)

#     class Meta:
#         model = User
#         fields = (
#             'email', 'id', 'username',
#             'first_name', 'last_name', 'is_subscribed')


# class IngredientsEditSerializer(serializers.ModelSerializer):

#     id = serializers.IntegerField()
#     amount = serializers.IntegerField()

#     class Meta:
#         model = Ingredient
#         fields = ('id', 'amount')


# class GetIngredientsMixin:

#     def get_ingredients(self, obj):
#         return obj.ingredients.values(
#             'id', 'name', 'measurement_unit',
#             amount=F('ingredients_amount__amount')
#         )


# class RecipeWriteSerializer(GetIngredientsMixin, serializers.ModelSerializer):
#     image = Base64ImageField(
#         source='image',
#         max_length=None,
#         use_url=True)
#     tags = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Tag.objects.all())
#     ingredients = IngredientsEditSerializer(
#         many=True)

#     class Meta:
#         model = Recipe
#         fields = '__all__'
#         read_only_fields = ('author',)

#     def validate(self, data):
#         ingredients = self.initial_data.get('ingredients')
#         ingredient_list = []
#         for _ in ingredients:
#             ingredient = get_object_or_404(
#                 Ingredient,
#                 id=_['id'])
#             if ingredient in ingredient_list:
#                 raise serializers.ValidationError(
#                     'ингредиент должен быть уникальным.')
#             ingredient_list.append(ingredient)
#         tags = self.initial_data.get('tags')
#         if not tags:
#             raise serializers.ValidationError(
#                 'Нужен хотя бы один тэг для рецепта.')
#         for tag_id in tags:
#             if not Tag.objects.filter(id=tag_id).exists():
#                 raise serializers.ValidationError(
#                     f'тэга с id = {tag_id} не существует.')
#         return data

#     def validate_cooking_time(self, cooking_time):
#         if int(cooking_time) < 1:
#             raise serializers.ValidationError(
#                 'Время приготовления >= 1.')
#         return cooking_time

#     def validate_ingredients(self, ingredients):
#         if not ingredients:
#             raise serializers.ValidationError(
#                 'Мин. 1 ингредиент в рецепте.')
#         for ingredient in ingredients:
#             if int(ingredient.get('amount')) < 1:
#                 raise serializers.ValidationError(
#                     'Количество ингредиента >= 1.')
#         return ingredients

#     def create_ingredients(self, ingredients, recipe):
#         ings = [
#             ingredient(
#                 recipe=recipe,
#                 ingredient_id=ingredient.get('id'),
#                 amount=ingredient.get('amount')
#             )
#             for ingredient in ingredients
#         ]
#         RecipeIngredient.objects.bulk_create(ings)

#     def create(self, validated_data):
#         validated_data.pop('recipe')
#         tags = self.initial_data.pop('tags')
#         ingredients = self.initial_data.pop('ingredients')
#         recipe = Recipe.objects.create(**validated_data)
#         recipe.tags.set(tags)
#         self.create_ingredients(ingredients, recipe)
#         return recipe

#     def update(self, instance, validated_data):
#         if 'ingredients' in validated_data:
#             ingredients = validated_data.pop('ingredients')
#             instance.ingredients.clear()
#             self.create_ingredients(ingredients, instance)
#         if 'tags' in validated_data:
#             instance.tags.set(
#                 validated_data.pop('tags'))
#         return super().update(
#             instance, validated_data)

#     def to_representation(self, instance):
#         return RecipeReadSerializer(
#             instance,
#             context={
#                 'request': self.context.get('request')
#             }).data


# class RecipeReadSerializer(GetIngredientsMixin, serializers.ModelSerializer):
#     image = Base64ImageField(max_length=None, use_url=True, source='image')
#     tags = TagSerializer(
#         many=True,
#         read_only=True)
#     author = RecipeUserSerializer(
#         read_only=True,
#         default=serializers.CurrentUserDefault())
#     ingredients = RecipeIngredientSerializer(
#         many=True,
#         required=True,
#         source='recipe')
#     is_favorited = serializers.BooleanField(
#         read_only=True)
#     is_in_shopping_cart = serializers.BooleanField(
#         read_only=True)

#     class Meta:
#         model = Recipe
#         fields = '__all__'


# class SubscribeRecipeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time')


# class SubscribeSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(
#         source='author.id')
#     email = serializers.EmailField(
#         source='author.email')
#     username = serializers.CharField(
#         source='author.username')
#     first_name = serializers.CharField(
#         source='author.first_name')
#     last_name = serializers.CharField(
#         source='author.last_name')
#     recipes = serializers.SerializerMethodField()
#     is_subscribed = serializers.BooleanField(
#         read_only=True)
#     recipes_count = serializers.IntegerField(
#         read_only=True)

#     class Meta:
#         model = Subscribe
#         fields = (
#             'email', 'id', 'username', 'first_name', 'last_name',
#             'is_subscribed', 'recipes', 'recipes_count',)

from django.conf import settings
#     def get_recipes(self, obj):
#         request = self.context.get('request')
#         limit = request.GET.get('recipes_limit')
#         recipes = (
#             obj.author.recipe.all()[:int(limit)] if limit
#             else obj.author.recipe.all())
#         return SubscribeRecipeSerializer(
#             recipes,
#             many=True).data
from django.contrib.auth import get_user_model
from django.db.models import F
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from recipes.models import (FavoriteRecipe, Follow, Ingredient,
                            IngredientInRecipe, Recipe, ShoppingCart, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class GetIsSubscribedMixin:
    """Отображение подписки на пользователя"""
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Создание пользователя"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password',)


class CustomUserListSerializer(GetIsSubscribedMixin, UserSerializer):
    """Просмотр пользователя"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        read_only_fields = ('is_subscribed', )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class GetIngredientsMixin:
    """Рецепты, получение ингредиентов"""

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('ingredients_amount__amount')
        )


class RecipeReadSerializer(GetIngredientsMixin, serializers.ModelSerializer):
    """Чтение рецептов"""
    tags = TagSerializer(many=True)
    author = CustomUserListSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeWriteSerializer(GetIngredientsMixin, serializers.ModelSerializer):
    """Запись рецептов"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def validate(self, data):
        ingredients = self.initial_data['ingredients']
        ingredient_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Минимально должен быть 1 ингредиент.'
            )
        for item in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=item['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиент не должен повторяться.'
                )
            if int(item.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Минимальное количество = 1'
                )
            ingredient_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def validate_cooking_time(self, time):
        if int(time) < 1:
            raise serializers.ValidationError(
                'Минимальное время = 1'
            )
        return time

    def add_ingredients_and_tags(self, instance, **validate_data):
        ingredients = validate_data['ingredients']
        tags = validate_data['tags']
        for tag in tags:
            instance.tags.add(tag)

        IngredientInRecipe.objects.bulk_create([
            IngredientInRecipe(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        ])
        return instance

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        return self.add_ingredients_and_tags(
            recipe, ingredients=ingredients, tags=tags
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = self.add_ingredients_and_tags(
            instance, ingredients=ingredients, tags=tags)
        return super().update(instance, validated_data)


class RecipeAddingSerializer(serializers.ModelSerializer):
    """Добавление рецепта в подписки"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(GetIsSubscribedMixin, serializers.ModelSerializer):
    """Подписка"""
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.author.recipes.all()
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeAddingSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.all().count()


class CheckSubscribeSerializer(serializers.ModelSerializer):
    """Проверка подписки"""
    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, obj):
        user = obj['user']
        author = obj['author']
        subscribed = user.follower.filter(author=author).exists()

        if self.context.get('request').method == 'POST':
            if user == author:
                raise serializers.ValidationError(
                    'Ошибка, на себя подписка не разрешена'
                )
            if subscribed:
                raise serializers.ValidationError(
                    'Ошибка, вы уже подписались'
                )
        if self.context.get('request').method == 'DELETE':
            if user == author:
                raise serializers.ValidationError(
                    'Ошибка, отписка от самого себя не разрешена'
                )
            if not subscribed:
                raise serializers.ValidationError(
                    {'errors': 'Ошибка, вы уже отписались'}
                )
        return obj


class CheckFavoriteSerializer(serializers.ModelSerializer):
    """Проверка избранного"""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')

    def validate(self, obj):
        user = self.context['request'].user
        recipe = obj['recipe']
        favorite = user.favorites.filter(recipe=recipe).exists()

        if self.context.get('request').method == 'POST' and favorite:
            raise serializers.ValidationError(
                'Этот рецепт уже добавлен в избранном'
            )
        if self.context.get('request').method == 'DELETE' and not favorite:
            raise serializers.ValidationError(
                'Этот рецепт отсутствует в избранном'
            )
        return obj


class CheckShoppingCartSerializer(serializers.ModelSerializer):
    """Проверка корзины"""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, obj):
        user = self.context['request'].user
        recipe = obj['recipe']
        cart = user.cart.filter(recipe=recipe).exists()

        if self.context.get('request').method == 'POST' and cart:
            raise serializers.ValidationError(
                'Этот рецепт уже добавлен в корзину'
            )
        if self.context.get('request').method == 'DELETE' and not cart:
            raise serializers.ValidationError(
                'Этот рецепт отсутствует в корзине'
            )
        return obj
