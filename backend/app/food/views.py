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


class BasicViewSet(viewsets.ModelViewSet):
    pagination_class = None
    http_method_names = ['get', 'head']
    permission_classes = (AllowAny,)


class TagViewSet(BasicViewSet, viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(BasicViewSet, viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.select_related(
        'author').prefetch_related('ingredients', 'tags').all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    def _perform_post(self, request, objs, recipe, error_msg):
        user = self.request.user
        if objs.exists():
            raise exceptions.ValidationError(
                error_msg
            )
        objs.model.objects.create(user=user, recipe=recipe)
        serializer = RecipeSubscriptionFavoritesShopSerializer(
            recipe,
            context={'request': request}
        )
        return serializer

    def _perform_delete(self, obj, error_msg):
        if not obj.exists():
            raise exceptions.ValidationError(
                error_msg
            )
        obj.delete()
        return True

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
            serializer = self._perform_post(request, favorite,
                                            recipe, 'Рецепт уже в избранном.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if self._perform_delete(favorite, 'В избранном рецепт не найден.'):
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
            serializer = self._perform_post(request, shopping_cart,
                                            recipe, 'Рецепт уже в корзине.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if self._perform_delete(shopping_cart,
                                    'В корзине рецепт не найден!.'):
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
