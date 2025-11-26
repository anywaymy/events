from django.contrib import admin

from .models import Events


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)

    prepopulated_fields = {'slug': ('title',)}

    readonly_fields = ('created_at',)

    fieldsets = (
        # Группировка полей
        ('Основная информация', {
            'fields': ('title', 'slug', 'content', "image", 'date_of_events', 'max_places')}
        ),

        ('Доп информация', {
            'fields': ('location', 'duration')}
         ),

        ('Временные метки', {
            'fields': ('created_at',)}
        )
    )