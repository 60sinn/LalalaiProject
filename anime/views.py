# anime/views.py
from django.shortcuts import render, get_object_or_404
from .models import Anime, Season, Episode

def anime_list(request):
    animes = Anime.objects.all()
    return render(request, 'anime/anime_list.html', {'animes': animes})

def anime_detail(request, anime_url_title):
    anime = get_object_or_404(Anime, url_title=anime_url_title)  # Извлекаем аниме по url_title
    seasons = anime.seasons.all()  # Получаем все сезоны для этого аниме
    return render(request, 'anime/anime_detail.html', {'anime': anime, 'seasons': seasons})

def season_detail(request, anime_url_title, season_url_title):
    anime = get_object_or_404(Anime, url_title=anime_url_title)
    season = get_object_or_404(Season, anime=anime, url_title=season_url_title)  # Получаем сезон по season_url_title
    episodes = season.episodes.all()  # Получаем все эпизоды сезона
    return render(request, 'anime/season_detail.html', {'season': season, 'episodes': episodes})

def episode_detail(request, anime_url_title, season_url_title, episode_url_title):
    anime = get_object_or_404(Anime, url_title=anime_url_title)
    season = get_object_or_404(Season, anime=anime, url_title=season_url_title)
    episode = get_object_or_404(Episode, season=season, url_title=episode_url_title)  # Получаем эпизод по episode_url_title
    return render(request, 'anime/episode_detail.html', {'episode': episode})
