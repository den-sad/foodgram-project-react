from distutils.util import strtobool
from django_filters import rest_framework
from .models import Recipes, Tag
from users.models import Favorites, ShoppingCart


CHOICES = (
    ('0', 'False'),
    ('1', 'True')
)


class RecipeFilter(rest_framework.FilterSet):
    is_favorited = rest_framework.ChoiceFilter(
        choices=CHOICES,
        method='get_is_favorited'
    )
    is_in_shopping_cart = rest_framework.ChoiceFilter(
        choices=CHOICES,
        method='get_shopping_cart_method'
    )
    author = rest_framework.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipes.objects.none()

        favorites = Favorites.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in favorites]
        fav_queryset = queryset.filter(id__in=recipes)
        if not strtobool(value):
            return queryset.difference(fav_queryset)
        return queryset.filter(id__in=recipes)

    def get_shopping_cart_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipes.objects.none()

        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_cart]
        shop_queryset = queryset.filter(id__in=recipes)

        if not strtobool(value):
            return queryset.difference(shop_queryset)
        return queryset.filter(id__in=recipes)

    class Meta:
        model = Recipes
        fields = ('author', 'tags')
