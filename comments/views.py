from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import AnimeComment, SeasonComment, EpisodeComment, ShortComment
from anime.models import Anime, Season, Episode
from shorts.models import Short
from django.core.paginator import Paginator

# --- лимиты ---(для будущего апдейта)
MAX_SHORT_COMMENT_LENGTH = 500
MAX_ANIME_COMMENT_LENGTH = 1000
MAX_SEASON_COMMENT_LENGTH = 1000
MAX_EPISODE_COMMENT_LENGTH = 1000

# ---------- для шортсов ----------
@require_POST
@login_required
def post_short_comment(request, short_id):
    short = get_object_or_404(Short, url_id=short_id)
    text = request.POST.get('text', '').strip()

    if not text:
        return JsonResponse({'success': False, 'error': 'Комментарий пустой'}, status=400)

    if len(text) > MAX_SHORT_COMMENT_LENGTH:
        return JsonResponse({'success': False, 'error': 'Комментарий слишком длинный'}, status=400)

    ShortComment.objects.create(short=short, author=request.user, text=text)
    return JsonResponse({'success': True})


def get_short_comments(request, short_id):
    short = get_object_or_404(Short, url_id=short_id)
    comments = short.comments.select_related('author').order_by('-created_at')
    
    data = []
    for c in comments:
        avatar_url = c.author.avatar.url if c.author.avatar and hasattr(c.author.avatar, 'url') \
            else f"https://ui-avatars.com/api/?name={c.author.username}&background=ecd5fa&color=8e44ad"

        data.append({
            'author': c.author.username,
            'avatar': avatar_url,
            'text': c.text,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        })

    return JsonResponse({'comments': data})


# ---------- для аниме ----------
@require_POST
@login_required
def post_anime_comment(request, slug):
    anime = get_object_or_404(Anime, url_title=slug)
    text = request.POST.get('text', '').strip()

    if not text:
        return JsonResponse({'success': False, 'error': 'Комментарий пустой'}, status=400)

    if len(text) > MAX_ANIME_COMMENT_LENGTH:
        return JsonResponse({'success': False, 'error': 'Комментарий слишком длинный'}, status=400)

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
        'is_last_page': not page_obj.has_next(),
    })


# ---------- для сезонов ----------
@require_POST
@login_required
def post_season_comment(request, season_slug):
    season = get_object_or_404(Season, url_title=season_slug)
    text = request.POST.get('text', '').strip()

    if not text:
        return JsonResponse({'success': False, 'error': 'Комментарий пустой'}, status=400)

    if len(text) > MAX_SEASON_COMMENT_LENGTH:
        return JsonResponse({'success': False, 'error': 'Комментарий слишком длинный'}, status=400)

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

    if not text:
        return JsonResponse({'success': False, 'error': 'Комментарий пустой'}, status=400)

    if len(text) > MAX_EPISODE_COMMENT_LENGTH:
        return JsonResponse({'success': False, 'error': 'Комментарий слишком длинный'}, status=400)

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
