from django.core.exceptions import ValidationError
from django.conf import settings
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