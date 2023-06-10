from django.contrib import admin
from .models import Tag, Measurement_units, Ingredients

admin.site.register(Tag)
admin.site.register(Ingredients)
admin.site.register(Measurement_units)
