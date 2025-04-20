# anime/views.py
from django.shortcuts import render, get_object_or_404
from .models import Anime, Season, Episode
from django.http import JsonResponse

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
    episode = get_object_or_404(Episode, season=season, url_title=episode_url_title)

    # Предыдущая серия
    prev_episode = Episode.objects.filter(
        season=season,
        episode_number__lt=episode.episode_number
    ).order_by('-episode_number').first()

    if not prev_episode:
        prev_season = Season.objects.filter(
            anime=anime,
            season_number__lt=season.season_number
        ).order_by('-season_number').first()
        if prev_season:
            prev_episode = Episode.objects.filter(
                season=prev_season
            ).order_by('-episode_number').first()

    # Следующая серия
    next_episode = Episode.objects.filter(
        season=season,
        episode_number__gt=episode.episode_number
    ).order_by('episode_number').first()

    if not next_episode:
        next_season = Season.objects.filter(
            anime=anime,
            season_number__gt=season.season_number
        ).order_by('season_number').first()
        if next_season:
            next_episode = Episode.objects.filter(
                season=next_season
            ).order_by('episode_number').first()

    return render(request, 'anime/episode_detail.html', {
        'episode': episode,
        'prev_episode': prev_episode,
        'next_episode': next_episode,
    })

from django.shortcuts import get_object_or_404, render
from .models import Anime, Opening

def opening_view(request, anime_url_title):
    anime = get_object_or_404(Anime, url_title=anime_url_title)
    openings = anime.openings.all()

    return render(request, 'anime/opening_detail.html', {
        'anime': anime,
        'openings': openings
    })

def opening_list_view(request, anime_url_title):
    anime = get_object_or_404(Anime, url_title=anime_url_title)
    openings = anime.openings.all()
    return render(request, 'anime/opening_list.html', {
        'anime': anime,
        'openings': openings
    })

def opening_detail_view(request, anime_url_title, url_title):
    anime = get_object_or_404(Anime, url_title=anime_url_title)
    opening = get_object_or_404(anime.openings, url_title=url_title)
    return render(request, 'anime/opening_detail.html', {
        'anime': anime,
        'opening': opening
    })


def get_seasons(request):
    anime_id = request.GET.get('anime_id')
    seasons = Season.objects.filter(anime_id=anime_id).values('id', 'title')
    return JsonResponse({'seasons': list(seasons)})