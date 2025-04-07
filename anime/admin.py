from django.contrib import admin
from .models import Genre, Studio, Anime, Season, Episode, Opening
from django.utils.html import format_html

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'studio', 'poster_preview')  # заменили
    search_fields = ('title',)
    list_filter = ('studio', 'release_date')
    readonly_fields = ('poster_preview',)  # можно использовать и в форме

    def poster_preview(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" style="width:60px; height:60px; object-fit:cover; border-radius:8px;" />',
                obj.poster.url
            )
        return "—"
    poster_preview.short_description = "Постер"

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('anime', 'season_number', 'title', 'release_date')
    list_filter = ('anime', 'season_number')

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'episode_number', 'title', 'release_date', 'video_preview', 'video_url')
    list_filter = ('season__anime', 'season')
    readonly_fields = ('video_preview', 'video_url')

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="250" controls>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>',
                obj.video.url
            )
        return "—"
    video_preview.short_description = "Превью"

    def video_url(self, obj):
        return obj.video.url if obj.video else "—"
    video_url.short_description = "Ссылка на видео"

@admin.register(Opening)
class OpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'anime', 'video_preview', 'video_url')
    list_filter = ('anime',)
    search_fields = ('title',)
    readonly_fields = ('video_preview', 'video_url')

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="250" controls>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>',
                obj.video.url
            )
        return "—"
    video_preview.short_description = "Превью"

    def video_url(self, obj):
        return obj.video.url if obj.video else "—"
    video_url.short_description = "Ссылка на видео"