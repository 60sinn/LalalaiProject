from django.shortcuts import render, get_object_or_404
from .models import Short
import random
 
def shorts_feed(request):
    shorts = list(Short.objects.all())
    random.shuffle(shorts)
    return render(request, 'shorts/feed.html', {'shorts': shorts})
 
def short_detail(request, url_id):
    short = get_object_or_404(Short, url_id=url_id)
    return render(request, 'shorts/detail.html', {'short': short})