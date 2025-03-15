import re
from django.core.exceptions import ValidationError


YOUTUBE_URL_PATTERN = re.compile(
    r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$'
)

def youtube_link_validator(value):
    """Валидатор для проверки ссылок на YouTube"""
    if not YOUTUBE_URL_PATTERN.match(value):
        raise ValidationError("Разрешены только ссылки на YouTube.")