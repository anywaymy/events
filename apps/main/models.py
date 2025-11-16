from django.db import models
from django.utils.text import slugify

from apps.users.validators import validate_image_format


def event_directory_path(instance, filename):
    return f"events/{instance.slug}/{filename}"


class Events(models.Model):
    title = models.CharField(max_length=250, unique=True, help_text="Введите название мероприятия")
    slug = models.SlugField(max_length=250, unique=True, help_text="Автоматически заполнится содержимым поля 'title'")
    content = models.TextField(max_length=500, help_text="Введите описание мероприятия")
    image = models.ImageField(upload_to=event_directory_path,
                              null=True, blank=True,
                              help_text="Выберите изображения вашего мероприятия",
                              validators=[validate_image_format],
                              default="")
    location = models.CharField(max_length=250, help_text="Место проведения", default='')
    date_of_events = models.DateTimeField(help_text="Дата проведения")
    duration = models.CharField(max_length=9, help_text="Длительность", default='')
    max_places = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def free_places(self):
        booked = self.bookings.count()
        return self.max_places - booked

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-created_at']