# from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator
from .models import Tag, Ingredients, Recipes, RecipeIngredients
from users.serializers import UserSerializer
from users.models import Favorites, ShoppingCart


class TagSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField(
        method_name='get_color'
    )

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id',)

    def get_color(self, obj):
        return str(obj.color).upper()


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id',)


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(method_name='get_recipe_id')
    name = serializers.SerializerMethodField(method_name='get_recipe_name')
    measurement_unit = serializers.SerializerMethodField(
        method_name='get_ingredient_measurement_unit'
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_recipe_id(self, obj):
        return obj.ingredient.id

    def get_recipe_name(self, obj):
        return obj.ingredient.name

    def get_ingredient_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Не задано dhtvz приготовления!'
            ),
        )
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )

    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('id', 'author')

    def get_ingredients(self, obj):
        ingredients = RecipeIngredients.objects.select_related(
            'ingredient').filter(recipe=obj)
        serializer = IngredientsRecipeSerializer(ingredients, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorites.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipeSubscriptionFavoritesShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class CreateUpdateIngredientsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Не задано количество!'
            ),
        )
    )

    class Meta:
        model = Ingredients
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = CreateUpdateIngredientsRecipesSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Не задано время приготовления!'
            ),
        )
    )

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError({
                'tags': 'Отсутствует тег.'
            })
        tags_set = set(tags)
        if len(tags) != len(tags_set):
            raise ValidationError({
                'tags': 'Дублирование тэгов.'
            })
        return value

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError({
                'ingredients': 'Не указан ингредиент.'
            })

        ingredient_list = [row['id'] for row in ingredients]
        ingredients_set = set(ingredient_list)
        if len(ingredient_list) != len(ingredients_set):
            raise ValidationError({
                'tags': 'Дублирование ингредиентов.'
            })
        return value

    def _get_ingredient_data(self, ingredient):
        amount = ingredient['amount']
        ingredient = get_object_or_404(Ingredients, pk=ingredient['id'])
        return (ingredient, amount)

    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        for item in ingredients:
            ingredient, amount = self._get_ingredient_data(item)
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.set(tags)

        if ingredients is not None:
            instance.ingredients.clear()

            for item in ingredients:
                ingredient, amount = self._get_ingredient_data(item)
                RecipeIngredients.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient,
                    defaults={'amount': amount}
                )

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        )

        return serializer.data
