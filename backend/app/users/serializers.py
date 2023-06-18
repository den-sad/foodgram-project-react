from rest_framework import serializers
from .models import User, Subscriptions
from food.models import Recipes


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscriptions.objects.filter(user=user, author=obj).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        read_only_fields = ('id',)


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True,
                                     'required': True}}

    def create(self, validated_data):
        if "password" in self.initial_data:
            from django.contrib.auth.hashers import make_password
            validated_data["password"] = make_password(
                self.initial_data['password'])
        else:
            raise serializers.ValidationError(
                {"password": ["Обязательное поле."]})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in self.initial_data:
            from django.contrib.auth.hashers import make_password
            validated_data["password"] = make_password(
                self.initial_data['password'])
        else:
            raise serializers.ValidationError(
                {"password": ["Обязательное поле."]})
        return super().update(instance, validated_data)


class SubscriptionsSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    def get_recipe_for_subscription(self):
        from food.serializers import RecipeSubscriptionFavoritesShopSerializer
        return RecipeSubscriptionFavoritesShopSerializer

    def get_recipes(self, obj):
        author_recipes = Recipes.objects.filter(author=obj)
        if 'recipes_limit' in self.context.get('request').GET:
            recipes_limit = self.context.get('request').GET['recipes_limit']
            author_recipes = author_recipes[:int(recipes_limit)]
        if author_recipes:
            serializer = self.get_recipe_for_subscription()(
                author_recipes,
                context={'request': self.context.get('request')},
                many=True
            )
            return serializer.data
        return []

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj).count()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
