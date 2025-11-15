from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import User, UserMessage

# После удаления пользователя, удаляем его изображение
@receiver(post_delete, sender=User)
def delete_user_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)

# После создания пользователя, создаём для него объект сообщения
@receiver(post_save, sender=User)
def send_success_registration_message(sender, instance, created, **kwargs):
    if created:
        msg = 'Ваш аккаунт успешно создан'
        UserMessage.objects.create(user=instance, message=msg)
