import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import User, Subscriptions


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        read_only_fields = ('id',)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscriptions.objects.filter(user=user, author=obj).exists()


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True,
                                     'required': True}}
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=['email', 'username']
        ), ]

    def _check_create_password(self):
        if "password" in self.initial_data:
            from django.contrib.auth.hashers import make_password
            password = make_password(
                self.initial_data['password'])
        else:
            raise serializers.ValidationError(
                {"password": ["Обязательное поле."]})
        return password

    def create(self, validated_data):
        validated_data["password"] = self._check_create_password()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["password"] = self._check_create_password()
        return super().update(instance, validated_data)

    def validate_username(self, data):
        username = data
        res = re.sub('^[\\w.@+-]+\\Z', "", username, count=0, flags=0)
        if res != '':
            raise serializers.ValidationError(
                "username пользователя не соответствует формату")
        res = re.sub(r'^[\/()* .+-:;"\']', "", username, count=0, flags=0)
        if res != username:
            raise serializers.ValidationError(
                "username пользователя не должен начинаться со спецсимвола")
        return data

    def validate_email(self, data):
        email = data
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "email уже зарегистрирован")
        res = re.sub(
            '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', "",
            email, count=0, flags=0)
        if res != email:
            raise serializers.ValidationError(
                "email не может содержать IP адрес")
        res = re.sub(r'^[\\\/()\* .+-:;"\']', "", email, count=0, flags=0)
        if res != email:
            raise serializers.ValidationError(
                "email не может начинаться спецсимволами")
        res = re.sub('[а-яА-Я]?', "", email, count=0, flags=0)
        if res != email:
            raise serializers.ValidationError(
                "email символы кирилицы недопустимы")
        res = re.sub('^\\S+@\\S+\\.\\S+$', "", email, count=0, flags=0)
        if res != '':
            raise serializers.ValidationError(
                "email неверного формата")
        return data


class SubscriptionsSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipe_for_subscription(self):
        from food.serializers import RecipeSubscriptionFavoritesShopSerializer
        return RecipeSubscriptionFavoritesShopSerializer

    def get_recipes(self, obj):
        author_recipes = obj.recipes.all()
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
        return obj.recipes.count()
