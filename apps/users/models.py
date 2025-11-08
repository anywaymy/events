from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models

from apps.users.validators import validate_image_format


def user_directory_path(instance, filename):
    return f"{instance.username}/users/images/{filename}"

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('user', 'user'),
    ]

    email = models.EmailField(max_length=250, validators=[EmailValidator], help_text="Введите email")
    image = models.ImageField(upload_to=user_directory_path,
                              null=True, blank=True,
                              help_text="Выберите изображения вашего профиля",
                              validators=[validate_image_format])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']