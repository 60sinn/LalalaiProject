from django.contrib import admin
from .models import Genre, Studio, Anime, Season, Episode

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'studio', 'get_poster_url')
    search_fields = ('title',)
    list_filter = ('studio', 'release_date')

    def get_poster_url(self, obj):
        return obj.poster_url  # возвращаем ссылку на постер
    get_poster_url.short_description = 'Poster URL'

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('anime', 'season_number', 'title', 'release_date')
    list_filter = ('anime', 'season_number')

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'episode_number', 'title', 'release_date', 'url')
    list_filter = ('season', 'episode_number')