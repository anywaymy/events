from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('username', 'created_at')
    search_fields = ('username', 'email')

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        # Группировка полей
        ('Основная информация', {
            'fields': ('username', 'email', 'image', 'role'),
        }),

        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
        })
    )