from itertools import chain
from django.contrib import admin
from .models import Tag, Ingredients, Recipes, RecipeIngredients, RecipeTags


class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
    )
    search_fields = ('name',)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit', 'name')


class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe',)


class RecipesAdmin(admin.ModelAdmin):
    def assigned_tags(self, obj):
        a = obj.tags.values_list('name')
        return list(chain.from_iterable(a))

    assigned_tags.short_description = 'Тэги'

    def favorites(self, obj):
        count = len(obj.favorites.values('user'))
        print(count)
        return count
    favorites.short_description = 'В избранном у пользователей, персон'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = Tag.objects.filter(is_author=True)
        return super(RecipesAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )

    exclude = ['tags']
    list_display = (
        'id',
        'name',
        'author',
        'assigned_tags',
        'favorites'
    )

    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')


admin.site.register(Tag, TagsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(RecipeTags)
