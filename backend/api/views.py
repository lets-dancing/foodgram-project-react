# import io

# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
# from django.db.models.aggregates import Count, Sum
# from django.db.models.expressions import Exists, OuterRef, Value
# from django.http import FileResponse
# from django.shortcuts import get_object_or_404
# from djoser.views import UserViewSet
# from .pagination import LimitPageNumberPagination
# from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
#                             Subscribe, Tag)
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfgen import canvas
# from rest_framework import generics, status, viewsets
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.decorators import action, api_view
# from rest_framework.permissions import (SAFE_METHODS, AllowAny,
#                                         IsAuthenticated,
#                                         IsAuthenticatedOrReadOnly)
# from rest_framework.response import Response

# from api.filters import IngredientFilter, RecipeFilter
# from api.permissions import IsAdminOrReadOnly

# from .serializers import (IngredientSerializer, RecipeWriteSerializer,
#                           SubscribeRecipeSerializer, SubscribeSerializer,
#                           TagSerializer, TokenSerializer, UserCreateSerializer,
#                           UserListSerializer, UserPasswordSerializer)

# User = get_user_model()
# FILENAME = 'shoppingcart.pdf'


# class GetObjectMixin:
#     """Миксин для удаления/добавления рецептов избранных/корзины."""

#     serializer_class = SubscribeRecipeSerializer
#     permission_classes = (AllowAny,)

#     def get_object(self):
#         recipe_id = self.kwargs['recipe_id']
#         recipe = get_object_or_404(Recipe, id=recipe_id)
#         self.check_object_permissions(self.request, recipe)
#         return recipe


# class PermissionAndPaginationMixin:
#     """Миксина для списка тегов и ингридиентов."""

#     permission_classes = (IsAdminOrReadOnly,)
#     pagination_class = None


# class AddAndDeleteSubscribe(
#         generics.RetrieveDestroyAPIView,
#         generics.ListCreateAPIView):
#     """Подписка и отписка от пользователя."""

#     serializer_class = SubscribeSerializer

#     def get_queryset(self):
#         return self.request.user.follower.select_related(
#             'following'
#         ).prefetch_related(
#             'following__recipe'
#         ).annotate(
#             recipes_count=Count('following__recipe'),
#             is_subscribed=Value(True), )

#     def get_object(self):
#         user_id = self.kwargs['user_id']
#         user = get_object_or_404(User, id=user_id)
#         self.check_object_permissions(self.request, user)
#         return user

#     def create(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if request.user.id == instance.id:
#             return Response(
#                 {'errors': 'На самого себя не подписаться!'},
#                 status=status.HTTP_400_BAD_REQUEST)
#         if request.user.follower.filter(author=instance).exists():
#             return Response(
#                 {'errors': 'Уже подписан!'},
#                 status=status.HTTP_400_BAD_REQUEST)
#         subs = request.user.follower.create(author=instance)
#         serializer = self.get_serializer(subs)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def perform_destroy(self, instance):
#         self.request.user.follower.filter(author=instance).delete()


# class AddDeleteFavoriteRecipe(
#         GetObjectMixin,
#         generics.RetrieveDestroyAPIView,
#         generics.ListCreateAPIView):
#     """Добавление и удаление рецепта в/из избранных."""

#     def create(self, request, *args, **kwargs):
#         instance = self.get_object()
#         request.user.favorite_recipe.recipe.add(instance)
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def perform_destroy(self, instance):
#         self.request.user.favorite_recipe.recipe.remove(instance)


# class AddDeleteShoppingCart(
#         GetObjectMixin,
#         generics.RetrieveDestroyAPIView,
#         generics.ListCreateAPIView):
#     """Добавление и удаление рецепта в/из корзины."""

#     def create(self, request, *args, **kwargs):
#         instance = self.get_object()
#         request.user.shopping_cart.recipe.add(instance)
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def perform_destroy(self, instance):
#         self.request.user.shopping_cart.recipe.remove(instance)


# class AuthToken(ObtainAuthToken):
#     """Авторизация пользователя."""

#     serializer_class = TokenSerializer
#     permission_classes = (AllowAny,)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response(
#             {'auth_token': token.key},
#             status=status.HTTP_201_CREATED)


# class UsersViewSet(UserViewSet):
#     """Пользователи."""

#     serializer_class = UserListSerializer
#     permission_classes = (AllowAny,)
#     pagination_class = LimitPageNumberPagination

#     def get_queryset(self):
#         return User.objects.annotate(
#             is_subscribed=Exists(
#                 self.request.user.follower.filter(
#                     author=OuterRef('id'))
#             )).prefetch_related(
#                 'follower', 'following'
#         ) if self.request.user.is_authenticated else User.objects.annotate(
#             is_subscribed=Value(False))

#     def get_serializer_class(self):
#         if self.request.method.lower() == 'post':
#             return UserCreateSerializer
#         return UserListSerializer

#     def perform_create(self, serializer):
#         password = make_password(self.request.data['password'])
#         serializer.save(password=password)

#     @action(
#         detail=False,
#         permission_classes=(IsAuthenticated,))
#     def subscriptions(self, request):
#         """Получить на кого пользователь подписан."""

#         user = request.user
#         queryset = Subscribe.objects.filter(user=user)
#         pages = self.paginate_queryset(queryset)
#         serializer = SubscribeSerializer(
#             pages, many=True,
#             context={'request': request})
#         return self.get_paginated_response(serializer.data)


# class RecipesViewSet(viewsets.ModelViewSet):
#     """Рецепты."""

#     queryset = Recipe.objects.all()
#     filterset_class = RecipeFilter
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     pagination_class = LimitPageNumberPagination

#     def get_serializer_class(self):
#         if self.request.method in SAFE_METHODS:
#             return RecipeWriteSerializer
#         return SubscribeRecipeSerializer

#     def get_queryset(self):
#         return Recipe.objects.annotate(
#             is_favorited=Exists(
#                 FavoriteRecipe.objects.filter(
#                     user=self.request.user, recipe=OuterRef('id'))),
#             is_in_shopping_cart=Exists(
#                 ShoppingCart.objects.filter(
#                     user=self.request.user,
#                     recipe=OuterRef('id')))
#         ).select_related('author').prefetch_related(
#             'tags', 'ingredients', 'recipe',
#             'shopping_cart', 'favorite_recipe'
#         ) if self.request.user.is_authenticated else Recipe.objects.annotate(
#             is_in_shopping_cart=Value(False),
#             is_favorited=Value(False),
#         ).select_related('author').prefetch_related(
#             'tags', 'ingredients', 'recipe',
#             'shopping_cart', 'favorite_recipe')

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     @action(
#         detail=False,
#         methods=['get'],
#         permission_classes=(IsAuthenticated,))
#     def download_shopping_cart(self, request):
#         """Качаем список с ингредиентами."""

#         buffer = io.BytesIO()
#         page = canvas.Canvas(buffer)
#         pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
#         x_position, y_position = 50, 800
#         page_count_before = 14
#         page_count_after = 24
#         shopping_cart = (
#             request.user.shopping_cart.recipe.
#             values(
#                 'ingredients__name',
#                 'ingredients__measurement_unit'
#             ).annotate(amount=Sum('recipe__amount')).order_by())
#         page.setFont('Vera', page_count_before)
#         if shopping_cart:
#             indent = 20
#             page.drawString(x_position, y_position, 'Cписок покупок:')
#             for index, recipe in enumerate(shopping_cart, start=1):
#                 page.drawString(
#                     x_position, y_position - indent,
#                     f'{index}. {recipe["ingredients__name"]} - '
#                     f'{recipe["amount"]} '
#                     f'{recipe["ingredients__measurement_unit"]}.')
#                 y_position -= 15
#                 position_limit = 50
#                 if y_position <= position_limit:
#                     page.showPage()
#                     y_position = 800
#             page.save()
#             buffer.seek(0)
#             return FileResponse(
#                 buffer, as_attachment=True, filename=FILENAME)
#         page.setFont('Vera', page_count_after)
#         page.drawString(
#             x_position,
#             y_position,
#             'Cписок покупок пуст!')
#         page.save()
#         buffer.seek(0)
#         return FileResponse(buffer, as_attachment=True, filename=FILENAME)


# class TagsViewSet(
#         PermissionAndPaginationMixin,
#         viewsets.ModelViewSet):
#     """Список тэгов."""

#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer


# class IngredientsViewSet(
#         PermissionAndPaginationMixin,
#         viewsets.ModelViewSet):
#     """Список ингредиентов."""

#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     filterset_class = IngredientFilter


# @api_view(['post'])
# def set_password(request):
#     """Изменить пароль."""

#     serializer = UserPasswordSerializer(
#         data=request.data,
#         context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             {'message': 'Пароль изменен!'},
#             status=status.HTTP_201_CREATED)
#     return Response(
#         {'error': 'Введите верные данные!'},
#         status=status.HTTP_400_BAD_REQUEST)

from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import BooleanField, Exists, OuterRef, Sum, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet

from recipes.models import (
    FavoriteRecipe, Ingredient, IngredientInRecipe, Recipe, ShoppingCart, Tag,
)
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrAdminOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    CheckFavoriteSerializer, CheckShoppingCartSerializer,
    CheckSubscribeSerializer, FollowSerializer, IngredientSerializer,
    RecipeAddingSerializer, RecipeReadSerializer, RecipeWriteSerializer,
    TagSerializer,
)

User = get_user_model()


class ListRetrieveViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    permission_classes = (IsAdminOrReadOnly, )


class TagViewSet(ListRetrieveViewSet):
    """Список тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    """Список ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Рецепты"""
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipe.objects.annotate(
                is_favorited=Exists(FavoriteRecipe.objects.filter(
                    user=self.request.user, recipe__pk=OuterRef('pk'))
                ),
                is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                    user=self.request.user, recipe__pk=OuterRef('pk'))
                )
            )
        else:
            return Recipe.objects.annotate(
                is_favorited=Value(False, output_field=BooleanField()),
                is_in_shopping_cart=Value(False, output_field=BooleanField())
            )

    @transaction.atomic()
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        data = {
            'user': request.user.id,
            'recipe': pk,
        }
        serializer = CheckFavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return self.add_object(FavoriteRecipe, request.user, pk)

    @favorite.mapping.delete
    def del_favorite(self, request, pk=None):
        data = {
            'user': request.user.id,
            'recipe': pk,
        }
        serializer = CheckFavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return self.delete_object(FavoriteRecipe, request.user, pk)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        data = {
            'user': request.user.id,
            'recipe': pk,
        }
        serializer = CheckShoppingCartSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return self.add_object(ShoppingCart, request.user, pk)

    @shopping_cart.mapping.delete
    def del_shopping_cart(self, request, pk=None):
        data = {
            'user': request.user.id,
            'recipe': pk,
        }
        serializer = CheckShoppingCartSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return self.delete_object(ShoppingCart, request.user, pk)

    @transaction.atomic()
    def add_object(self, model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeAddingSerializer(recipe)
        return Response(serializer.data, status=HTTPStatus.CREATED)

    @transaction.atomic()
    def delete_object(self, model, user, pk):
        model.objects.filter(user=user, recipe__id=pk).delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(
        methods=['get'], detail=False, permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total=Sum('amount'))
        result = settings.SHOPPIHG_LIST
        result += '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["total"]}/'
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ])
        response = HttpResponse(result, content_type='text/plain')
        content_disposition = f'attachment; filename={settings.FILENAME}'
        response['Content-Disposition'] = content_disposition
        return response


class FollowViewSet(UserViewSet):
    """Подписка"""
    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    @transaction.atomic()
    def subscribe(self, request, id=None):

        user = request.user
        author = get_object_or_404(User, pk=id)
        data = {
            'user': user.id,
            'author': author.id,
        }
        serializer = CheckSubscribeSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        result = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(result, context={'request': request})
        return Response(serializer.data, status=HTTPStatus.CREATED)

    @subscribe.mapping.delete
    @transaction.atomic()
    def del_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        data = {
            'user': user.id,
            'author': author.id,
        }
        serializer = CheckSubscribeSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user.follower.filter(author=author).delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
