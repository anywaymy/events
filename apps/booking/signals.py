from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import UserMessage

from .models import Booking


# После брони мероприятия, автоматом отправляем уведомление пользователю
@receiver(post_save, sender=Booking)
def send_success_booked_event(sender, instance, created, **kwargs):
    if created:
        msg = f'Вы успешно забронировали мероприятие "{instance.event.title}"'
        UserMessage.objects.create(user=instance.user, message=msg)
