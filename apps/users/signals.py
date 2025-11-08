from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User

@receiver(post_delete, sender=User)
def delete_user_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)