from django.db import models
from django.utils.text import slugify

class Events(models.Model):
    title = models.CharField(max_length=250, unique=True, help_text="Введите название мероприятия")
    slug = models.SlugField(max_length=250, unique=True, help_text="Автоматически заполнится содержимым поля 'title'")
    content = models.TextField(max_length=500, help_text="Введите описание мероприятия")
    date_of_events = models.DateTimeField(help_text="Дата проведения")
    created_at = models.DateTimeField(auto_now_add=True)

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