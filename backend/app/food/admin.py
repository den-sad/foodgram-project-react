from django.contrib import admin
from .models import Tag, Ingredients, Recipes, RecipeIngredients, RecipeTags


class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )

    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '------'


admin.site.register(Tag)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes)

admin.site.register(RecipeIngredients)
admin.site.register(RecipeTags)
