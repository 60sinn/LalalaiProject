from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from .validators import validate_avatar_file_size, validate_avatar_file_extension

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'
        MANAGER = 'manager', 'Менеджер по аниме'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER
    )

    bio = models.TextField(
        verbose_name='Описание профиля',
        max_length=500,
        blank=True,
        help_text='Расскажи о себе или напиши что-то крутое 🌟'
    )

    avatar = CloudinaryField('avatar', blank=True, null=True, validators=[validate_avatar_file_size, validate_avatar_file_extension])

    last_username_change = models.DateTimeField(null=True, blank=True)
    last_email_change = models.DateTimeField(null=True, blank=True)

    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    def is_manager(self):
        return self.role == self.Roles.MANAGER

    def is_admin(self):
        return self.role == self.Roles.ADMIN
