from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from food.models import Recipes


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.CharField(
        max_length=254,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['pk']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user_email'
            ),
        )

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    """Модель для хранения подкписок пользователя на авторов"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = (
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
        )

    def __str__(self):
        return f'Пользователь {self.userß} подписан на {self.author}'


class Favorites(models.Model):
    """Модель для хранения избранного пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorites'
            ),
        )

    def __str__(self):
        return f'Пользователь: {self.user}, избранный рецепт: {self.recipe} '


class ShoppingCart(models.Model):
    """
    Модель для хранения рецептов ингридиенты для которых необходимо купить.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Cписок покупок'
        verbose_name_plural = 'Список покупок'

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'Рецепт {self.recipe} в корзине у {self.user}'
