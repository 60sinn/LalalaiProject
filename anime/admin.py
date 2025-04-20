from django.contrib import admin
from django import forms
from cloudinary.uploader import upload_large
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

class EpisodeAdminForm(forms.ModelForm):
    anime = forms.ModelChoiceField(
        queryset=Anime.objects.all(),
        required=False,
        label="Аниме"
    )
    video_file = forms.FileField(required=False, label="Загрузить видео (большие файлы)")

    class Meta:
        model = Episode
        fields = [
            'anime',
            'season',
            'episode_number',
            'title',
            'description',
            'release_date',
            'url_title',
            'video',
            'video_file',
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        file = self.cleaned_data.get('video_file')
        if file:
            result = upload_large(file, resource_type='video', chunk_size=100_000_000)
            instance.video = result['secure_url']

        if commit:
            instance.save()
        return instance




@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    form = EpisodeAdminForm
    list_display = ('season', 'episode_number', 'title', 'release_date', 'video_preview', 'video_url')
    list_filter = ('season__anime', 'season')
    readonly_fields = ('video_preview', 'video_url')
    
    class Media:
        js = ('admin/js/episode_admin.js',)

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="250" controls>'
                '<source src="{}" type="video/mp4">'
                'Ваш браузер не поддерживает видео.'
                '</video>',
                obj.video
            )
        return "—"
    video_preview.short_description = "Превью"

    def video_url(self, obj):
        return obj.video if obj.video else "—"
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