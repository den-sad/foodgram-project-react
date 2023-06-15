from django.contrib import admin
from .models import User, Subscriptions


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')


admin.site.register(User)
admin.site.register(Subscriptions, SubscriptionsAdmin)
