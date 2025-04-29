from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import AnimeRating, SeasonRating
from anime.models import Anime, Season
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def rate_anime(request):
    if request.method == "POST":
        anime_id = request.POST.get("anime_id")
        score = int(request.POST.get("score", 0))
        
        if score < 1 or score > 10:
            return JsonResponse({"error": "Недопустимая оценка"}, status=400)
        
        anime = Anime.objects.filter(id=anime_id).first()
        if not anime:
            return JsonResponse({"error": "Аниме не найдено"}, status=404)

        rating, created = AnimeRating.objects.update_or_create(
            user=request.user,
            anime=anime,
            defaults={"score": score}
        )
        return JsonResponse({"success": True, "score": score})
    
    return JsonResponse({"error": "Неверный метод"}, status=405)


@login_required
@csrf_exempt
def rate_season(request):
    if request.method == "POST":
        season_id = request.POST.get("season_id")
        score = int(request.POST.get("score", 0))
        
        if score < 1 or score > 10:
            return JsonResponse({"error": "Недопустимая оценка"}, status=400)
        
        season = Season.objects.filter(id=season_id).first()
        if not season:
            return JsonResponse({"error": "Сезон не найден"}, status=404)

        rating, created = SeasonRating.objects.update_or_create(
            user=request.user,
            season=season,
            defaults={"score": score}
        )
        return JsonResponse({"success": True, "score": score})
    
    return JsonResponse({"error": "Неверный метод"}, status=405)