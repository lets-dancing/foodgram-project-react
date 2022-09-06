# from django.contrib.auth import get_user_model
# from django.core import validators
# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# User = get_user_model()


# class Ingredient(models.Model):
#     name = models.CharField(
#         'Название ингредиента',
#         max_length=200)
#     measurement_unit = models.CharField(
#         'Единица измерения ингредиента',
#         max_length=200)

#     class Meta:
#         ordering = ['name']
#         verbose_name = 'Ингредиент'
#         verbose_name_plural = 'Ингредиенты'

#     def __str__(self):
#         return f'{self.name}, {self.measurement_unit}.'


# class Tag(models.Model):
#     name = models.CharField(
#         'Имя',
#         max_length=60,
#         unique=True)
#     color = models.CharField(
#         'Цвет',
#         max_length=7,
#         unique=True)
#     slug = models.SlugField(
#         'Ссылка',
#         max_length=100,
#         unique=True)

#     class Meta:
#         verbose_name = 'Тэг'
#         verbose_name_plural = 'Тэги'
#         ordering = ['-id']

#     def __str__(self):
#         return self.name


# class Recipe(models.Model):
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='recipe',
#         verbose_name='Автор рецепта')
#     name = models.CharField(
#         'Рецепт',
#         max_length=255)
#     image = models.ImageField(
#         'Изображение блюда',
#         upload_to='recipes/',
#         blank=True,
#         null=True)
#     text = models.TextField('Описание рецепта')
#     cooking_time = models.BigIntegerField('Время приготовления')
#     ingredients = models.ManyToManyField(
#         Ingredient,
#         through='RecipeIngredient')
#     tags = models.ManyToManyField(
#         Tag,
#         verbose_name='Тэги',
#         related_name='recipes',)
#     pub_date = models.DateTimeField(
#         'Дата публикации',
#         auto_now_add=True,)
#     slug = models.SlugField(
#         max_length=50,
#         unique=True, null=True,
#         verbose_name='slug рецепта'
#     )

#     class Meta:
#         ordering = ['-pub_date']
#         verbose_name = 'Рецепт'
#         verbose_name_plural = 'Рецепты'

#     def __str__(self) -> str:
#         return f'{self.author.email}, {self.name}, slug {self.slug}'


# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='recipe')
#     ingredient = models.ForeignKey(
#         Ingredient,
#         on_delete=models.CASCADE,
#         related_name='ingredient')
#     amount = models.PositiveSmallIntegerField(
#         default=1,
#         validators=(
#             validators.MinValueValidator(
#                 1, message='Мин. количество ингридиентов 1'),),
#         verbose_name='Количество',)

#     class Meta:
#         verbose_name = 'Количество ингредиента'
#         verbose_name_plural = 'Количество ингредиентов'
#         ordering = ['-id']
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['recipe', 'ingredient'],
#                 name='unique ingredient')
#         ]


# class Subscribe(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='follower',
#         verbose_name='Подписчик')
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='following',
#         verbose_name='Подписка')
#     created = models.DateTimeField(
#         'Дата подписки',
#         auto_now_add=True)

#     class Meta:
#         ordering = ['user']
#         verbose_name = 'Подписка'
#         verbose_name_plural = 'Подписки'
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'author'],
#                 name='unique subs'),
#             models.CheckConstraint(
#                 check=~models.Q(user=models.F('author')),
#                 name='запрет подписки на самого себя',
#             ),
#         ]

#     def __str__(self):
#         return f'Пользователь: {self.user} - автор: {self.author}'


# class FavoriteRecipe(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         null=True,
#         related_name='favorite_recipe',
#         verbose_name='Пользователь')
#     recipe = models.ManyToManyField(
#         Recipe,
#         related_name='favorite_recipe',
#         verbose_name='Избранный рецепт'
#     )

#     class Meta:
#         verbose_name = 'Избранный рецепт'
#         verbose_name_plural = 'Избранные рецепты'

#     def __str__(self):
#         list_ = [item['name'] for item in self.recipe.values('name')]
#         return f'Пользователь {self.user} добавил {list_} в избранные.'

#     @receiver(post_save, sender=User)
#     def create_empty_favorite_recipe(
#             sender, instance, created, **kwargs):
#         if created:
#             FavoriteRecipe.objects.create(user=instance)


# class ShoppingCart(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='cart',
#         null=True,
#         verbose_name='Пользователь')
#     recipe = models.ManyToManyField(
#         Recipe,
#         related_name='cart',
#         verbose_name='Покупка')

#     class Meta:
#         verbose_name = 'Покупка'
#         verbose_name_plural = 'Покупки'
#         ordering = ['-id']

#     def __str__(self):
#         list_ = [item['name'] for item in self.recipe.values('name')]
#         return f'Пользователь {self.user} добавил {list_} в покупки.'

#     @receiver(post_save, sender=User)
#     def create_shopping_cart(
#             sender, instance, created, **kwargs):
#         if created:
#             return ShoppingCart.objects.create(user=instance)

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

User = get_user_model()


class Tag(models.Model):
    """Модель списка тегов"""
    name = models.CharField(
        verbose_name='Наименование тега',
        max_length=50,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Адресная ссылка',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента"""
    name = models.CharField(
        verbose_name='Наименование ингредиента',
        max_length=150
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Recipe(models.Model):
    """Модель рецепта"""
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=255
    )
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True,
        null=True,
        upload_to='image_recipes/',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(1, 'Время не может быть меньше 1 минуты.')
        ]
    )
    pud_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pud_date',)

    def __str__(self):
        return self.name

    def get_absoulute_url(self):
        return reverse('recipe', args=[self.pk])


class IngredientInRecipe(models.Model):
    """Промежуточная модель ингредиента и количества в рецепте"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amount',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_amount',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Минимальное количество ингредиента = 1')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}'


class FavoriteRecipe(models.Model):
    """Модель избранного рецепта"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe.name}'


class ShoppingCart(models.Model):
    """Модель список покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_user'
            )
        ]
