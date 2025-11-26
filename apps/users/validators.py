import os

from django.core.exceptions import ValidationError


def validate_image_format(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpeg', '.jpg', '.png']

    if ext not in valid_extensions:
        raise ValidationError(F'Недопустимый формат файлы {ext}. Разрешены только {', '.join(valid_extensions)}')

