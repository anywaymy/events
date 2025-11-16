from django.contrib import admin

from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "event__title")
    readonly_fields = ("booking_date",)
