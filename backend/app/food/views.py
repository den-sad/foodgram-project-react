from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import (TagSerializer, IngredientsSerializer,
                          RecipeSerializer, RecipeCreateUpdateSerializer,
                          RecipeSubscriptionFavoritesShopSerializer
                          )
from .models import Tag, Ingredients, Recipes
from users.models import Favorites, ShoppingCart
from .filters import RecipeFilter
from api.pagination import CustomPagination


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
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    @action(detail=True, methods=('post', 'delete'))
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

    @action(detail=True, methods=('post', 'delete'))
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
