from django.contrib import admin
from .models import User, PasswordResetToken, UserMessage

class UserMessageAdmin(admin.TabularInline):
    model = UserMessage
    extra = 1

    list_display = ('user', 'message')
    readonly_fields = ('created_at',)

    # fieldsets = (
    #     ('Сообщения пользователя', {
    #         'fields': ('message',)
    #     }),
    #
    #     ('Временные метки', {
    #         'fields': ('created_at',)
    #     }),
    # )

# админ панель для пользователя
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('username', 'created_at')
    search_fields = ('username', 'email')

    inlines = (UserMessageAdmin,)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        # Группировка полей
        ('Основная информация', {
            'fields': ('username', 'email', 'image', 'role'),
        }),

        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

# админ панель для токена
@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)
    readonly_fields = ('user', 'code', 'created_at')