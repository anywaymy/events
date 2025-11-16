from django.db import models

from apps.users.models import User
from apps.main.models import Events

class Booking(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='bookings', help_text="Выберите пользователя")
    event = models.ForeignKey(to=Events, on_delete=models.CASCADE, related_name='bookings', help_text="Выберите мероприятие")
    booking_date = models.DateTimeField(auto_now_add=True, help_text="Дата бронирования")

    def __str__(self):
        return "бронирование"

    class Meta:
        verbose_name = "бронирование"
        verbose_name_plural = "бронирование"
        unique_together = ('user', 'event')
        ordering = ["-booking_date"]