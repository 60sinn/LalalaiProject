from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'avatar_preview')  # добавили preview
    readonly_fields = ('avatar_preview',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'avatar', 'avatar_preview')}),  # добавили avatar в форму
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "—"
    avatar_preview.short_description = 'Аватар'
