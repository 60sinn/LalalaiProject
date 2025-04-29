from django.contrib import admin
from .models import Short
 
@admin.register(Short)
class ShortAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    list_filter = ('created_at', 'anime')

 