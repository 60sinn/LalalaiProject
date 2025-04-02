from django.contrib.auth.models import AbstractUser
from django.db import models

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

    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    def is_manager(self):
        return self.role == self.Roles.MANAGER

    def is_admin(self):
        return self.role == self.Roles.ADMIN
