from django.contrib import admin
from .models import Genre, Studio, Anime

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'studio')
    search_fields = ('title',)
    list_filter = ('studio', 'release_date')
