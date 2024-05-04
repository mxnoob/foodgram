from django.contrib import admin

from .models import User, Subscriber


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка для пользователя"""

    list_display = ('id', 'full_name', 'username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    search_help_text = 'Поиск по `username` и `email`'
    list_display_links = ('id', 'username', 'email', 'full_name')

    @admin.display(description='Имя фамилия')
    def full_name(self, obj):
        """Получение полного имени"""
        return obj.get_full_name()


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Админка подписок"""
