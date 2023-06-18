from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.pagination import CustomPagination
from users.models import Favorites, ShoppingCart
from .serializers import (TagSerializer, IngredientsSerializer,
                          RecipeSerializer, RecipeCreateUpdateSerializer,
                          RecipeSubscriptionFavoritesShopSerializer
                          )
from .models import Tag, Ingredients, Recipes, RecipeIngredients
from .filters import RecipeFilter
from .utils import make_pdf_file
from users.permissions import IsAuthorOrAdmin


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ['get', 'head']
    permission_classes = (AllowAny,)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    http_method_names = ['get', 'head']
    permission_classes = (AllowAny,)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipes, pk=pk)
        favorite = Favorites.objects.filter(
            user=user,
            recipe=recipe
        )

        if self.request.method == 'POST':
            if favorite.exists():
                raise exceptions.ValidationError(
                    'Рецепт уже в избранном.'
                )
            Favorites.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubscriptionFavoritesShopSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not favorite.exists():
                raise exceptions.ValidationError(
                    'В избранном рецепт не найден.'
                )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipes, pk=pk)
        shopping_cart = ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        )

        if self.request.method == 'POST':
            if shopping_cart.exists():
                raise exceptions.ValidationError(
                    'Рецепт уже в корзине.'
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubscriptionFavoritesShopSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not shopping_cart.exists():
                raise exceptions.ValidationError(
                    'В корзине рецепт не найден.'
                )
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        cart = ShoppingCart.objects.filter(user=self.request.user)
        recipes = [item.recipe for item in cart]
        amounts = RecipeIngredients.objects.filter(
            recipe__in=recipes).values('ingredient').annotate(
            amount=Sum('amount')
        )

        ingredients_list = []
        for item in amounts:
            ingredient = Ingredients.objects.get(pk=item['ingredient'])
            name = ingredient.name
            measure = ingredient.measurement_unit
            amount = item['amount']
            ingredients_list.append(
                f'{name}, {amount} {measure}'
            )
        pdf = make_pdf_file(ingredients_list)
        return FileResponse(pdf, as_attachment=True, filename="shop.pdf")
