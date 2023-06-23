from itertools import chain
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Tag, Ingredients, Recipes, RecipeIngredients, RecipeTags


class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

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


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    min_num = 1


class RecipeTagsInline(admin.TabularInline):
    model = RecipeTags
    min_num = 1


class RecipesAdmin(admin.ModelAdmin):

    inlines = [
        RecipeIngredientsInline,
        RecipeTagsInline,
    ]
    fields = (
        'author',
        'name',
        'image',
        'preview',
        'text',
        'cooking_time',
    )
    list_display = (
        'id',
        'preview',
        'name',
        'author',
        'assigned_tags',
        'favorites'
    )

    exclude = ['tags']
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(
            f'<img height="300" width="300" src="{obj.image.url}">'
        )

    def assigned_tags(self, obj):
        a = obj.tags.values_list('name')
        return list(chain.from_iterable(a))

    assigned_tags.short_description = 'Тэги'

    def favorites(self, obj):
        count = len(obj.favorites.values('user'))
        return count
    favorites.short_description = 'В избранном у пользователей, персон'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = Tag.objects.filter(is_author=True)
        return super(RecipesAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )


admin.site.register(Tag, TagsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(RecipeTags)
