import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Tag, Ingredients, Measurement_units


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientsSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SlugRelatedField(
        queryset=Measurement_units.objects.all(),
        slug_field='name')

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')
