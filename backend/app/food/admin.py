from itertools import chain
from django.contrib import admin
from .models import Tag, Ingredients, Recipes, RecipeIngredients, RecipeTags


class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )

    search_fields = ('name',)
    list_filter = ('measurement_unit', 'name')


class RecipesAdmin(admin.ModelAdmin):
    def assigned_tags(self, obj):
        a = obj.tags.values_list('name')
        return list(chain.from_iterable(a))

    assigned_tags.short_description = 'Тэги'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = Tag.objects.filter(is_author=True)
        return super(RecipesAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )

    list_display = (
        'name',
        'author',
        'assigned_tags',
    )

    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')


admin.site.register(Tag)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes, RecipesAdmin)

admin.site.register(RecipeIngredients)
admin.site.register(RecipeTags)
