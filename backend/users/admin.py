from django.contrib import admin

from .models import Subscriber, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка для пользователя"""

    list_display = ('id', 'full_name', 'username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    search_help_text = 'Поиск по `username` и `email`'
    list_display_links = ('id', 'username', 'email', 'full_name')

    def save_model(self, request, obj, form, change):
        """
        Хэширование и сохранение пароля.
        """
        if 'password' in form.changed_data and obj.password:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

    @admin.display(description='Имя фамилия')
    def full_name(self, obj):
        """Получение полного имени"""
        return obj.get_full_name()


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Админка подписок"""
