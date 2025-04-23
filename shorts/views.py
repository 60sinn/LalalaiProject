from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Short
import random
 
def shorts_feed(request):
    shorts = list(Short.objects.all())
    random.shuffle(shorts)
    return render(request, 'shorts/feed.html', {'shorts': shorts})
 
def short_detail(request, url_id):
    shorts = list(Short.objects.all())
    random.shuffle(shorts)
    return render(request, 'shorts/feed.html', {'shorts': shorts})

@login_required
@require_POST
def toggle_like(request, url_id):
    short = get_object_or_404(Short, url_id=url_id)
    user = request.user

    if user in short.likes.all():
        short.likes.remove(user)
        liked = False
    else:
        short.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': short.likes.count()
    })