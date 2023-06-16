from django.contrib import admin
from .models import User, Subscriptions


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username')
    list_filter = ('email', 'username', 'is_active')


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
