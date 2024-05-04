from django.contrib import admin

from .models import LinkMapped


@admin.register(LinkMapped)
class ShortenerAdmin(admin.ModelAdmin):
    """Админка Коротких ссылок"""
