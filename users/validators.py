from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import os

def validate_avatar_file_size(value):
    if not hasattr(value, 'size'):
        return

    max_kb = getattr(settings, 'MAX_AVATAR_SIZE_KB', 4096)
    if value.size > max_kb * 1024:
        raise ValidationError(f"Максимальный размер аватара — {max_kb}KB. Загружено: {value.size / 1024:.0f}KB.")
    
def validate_avatar_file_extension(value):
    if not hasattr(value, 'name'):
        return
    
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']  # ❌ gif исключён
    if ext not in allowed_extensions:
        raise ValidationError(f"Недопустимый формат файла: {ext}. Разрешены: {', '.join(allowed_extensions)}.")
    
def format_timedelta(td: timedelta):
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60

    parts = []
    if days > 0:
        parts.append(f"{days} дн")
    if hours > 0:
        parts.append(f"{hours} ч")
    if minutes > 0:
        parts.append(f"{minutes} мин")

    return " ".join(parts) if parts else "меньше минуты"

def validate_username_change(user):
    if user.last_username_change:
        delta = timezone.now() - user.last_username_change
        limit = timedelta(days=7)
        if delta < limit:
            remaining = format_timedelta(limit - delta)
            raise ValidationError(f"Ник можно менять раз в 7 дней. Осталось: {remaining}.")

def validate_email_change(user):
    if user.last_email_change:
        delta = timezone.now() - user.last_email_change
        limit = timedelta(days=30)
        if delta < limit:
            remaining = format_timedelta(limit - delta)
            raise ValidationError(f"Email можно менять раз в 30 дней. Осталось: {remaining}.")
