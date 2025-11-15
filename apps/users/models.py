import uuid
from uuid import uuid4

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models

from apps.users.validators import validate_image_format

# Функция, которая создаёт уникальную папку исходя из имени пользователя
def user_directory_path(instance, filename):
    return f"{instance.username}/users/images/{filename}"

# Модель пользователя
class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "admin"),
        ("user", "user"),
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
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]

# Модель токена для восстановления пароля
class PasswordResetToken(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4(), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.created_at < timezone.timedelta(hours=24)


    def __str__(self):
        return f"Токен восстановления для пользователя {self.user}"

# Модель сообщений для пользователя
class UserMessage(models.Model):
    user = models.ForeignKey(to=User,
                             related_name="user_messages",
                             on_delete=models.CASCADE,
                             help_text="Пользователь")
    message = models.TextField(max_length=500, help_text="Уведомление для пользователя")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания")

# class Profile(models.Model):
#     user = models.OneToOneField(to=User, on_delete=models.CASCADE)