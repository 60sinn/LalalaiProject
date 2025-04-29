from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import AnimeComment, SeasonComment, EpisodeComment, ShortComment
from anime.models import Anime, Season, Episode
from shorts.models import Short
from django.core.paginator import Paginator

# ---------- для шортсов ----------
@require_POST
@login_required
def post_short_comment(request, short_id):
    short = get_object_or_404(Short, url_id=short_id)
    text = request.POST.get('text', '').strip()

    if text:
        ShortComment.objects.create(short=short, author=request.user, text=text)

    return JsonResponse({'success': True})


def get_short_comments(request, short_id):
    short = get_object_or_404(Short, url_id=short_id)
    comments = short.comments.select_related('author').order_by('-created_at')
    
    data = []
    for c in comments:
        if c.author.avatar and hasattr(c.author.avatar, 'url'):
            avatar_url = c.author.avatar.url
        else:
            # Фолбэк с UI Avatars
            avatar_url = f"https://ui-avatars.com/api/?name={c.author.username}&background=ecd5fa&color=8e44ad"

        data.append({
            'author': c.author.username,
            'avatar': avatar_url,
            'text': c.text,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        })

    return JsonResponse({'comments': data})


# ---------- для анимешки<3 ----------
@require_POST
@login_required
def post_anime_comment(request, slug):
    anime = get_object_or_404(Anime, url_title=slug)
    text = request.POST.get('text', '').strip()

    if text:
        AnimeComment.objects.create(anime=anime, author=request.user, text=text)

    return JsonResponse({'success': True})


def get_anime_comments(request, slug):
    anime = get_object_or_404(Anime, url_title=slug)
    page = int(request.GET.get('page', 1))

    comments_qs = anime.comments.select_related('author').order_by('-created_at', '-id')
    paginator = Paginator(comments_qs, 10)
    page_obj = paginator.get_page(page)

    data = []
    for c in page_obj:
        avatar_url = c.author.avatar.url if c.author.avatar and hasattr(c.author.avatar, 'url') \
            else f"https://ui-avatars.com/api/?name={c.author.username}&background=ecd5fa&color=8e44ad"

        data.append({
            'id': c.id,
            'author': c.author.username,
            'avatar': avatar_url,
            'text': c.text,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        })

    return JsonResponse({
        'comments': data,
        'is_last_page': not page_obj.has_next(),  # 💡 вот оно
    })


# ---------- для сезонов ----------
@require_POST
@login_required
def post_season_comment(request, season_slug):
    season = get_object_or_404(Season, url_title=season_slug)
    text = request.POST.get('text', '').strip()

    if text:
        SeasonComment.objects.create(season=season, author=request.user, text=text)

    return JsonResponse({'success': True})


def get_season_comments(request, season_slug):
    season = get_object_or_404(Season, url_title=season_slug)
    page = int(request.GET.get('page', 1))

    comments_qs = season.comments.select_related('author').order_by('-created_at', '-id')
    paginator = Paginator(comments_qs, 10)
    page_obj = paginator.get_page(page)

    data = []
    for c in page_obj:
        avatar_url = c.author.avatar.url if c.author.avatar and hasattr(c.author.avatar, 'url') \
            else f"https://ui-avatars.com/api/?name={c.author.username}&background=ecd5fa&color=8e44ad"

        data.append({
            'id': c.id,
            'author': c.author.username,
            'avatar': avatar_url,
            'text': c.text,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        })

    return JsonResponse({
        'comments': data,
        'is_last_page': not page_obj.has_next(),
    })


# ---------- для серий ----------
@require_POST
@login_required
def post_episode_comment(request, episode_slug):
    episode = get_object_or_404(Episode, url_title=episode_slug)
    text = request.POST.get('text', '').strip()

    if text:
        EpisodeComment.objects.create(episode=episode, author=request.user, text=text)

    return JsonResponse({'success': True})


def get_episode_comments(request, episode_slug):
    episode = get_object_or_404(Episode, url_title=episode_slug)
    page = int(request.GET.get('page', 1))

    comments_qs = episode.comments.select_related('author').order_by('-created_at', '-id')
    paginator = Paginator(comments_qs, 10)
    page_obj = paginator.get_page(page)

    data = []
    for c in page_obj:
        avatar_url = c.author.avatar.url if c.author.avatar and hasattr(c.author.avatar, 'url') \
            else f"https://ui-avatars.com/api/?name={c.author.username}&background=ecd5fa&color=8e44ad"

        data.append({
            'id': c.id,
            'author': c.author.username,
            'avatar': avatar_url,
            'text': c.text,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        })

    return JsonResponse({
        'comments': data,
        'is_last_page': not page_obj.has_next(),
    })