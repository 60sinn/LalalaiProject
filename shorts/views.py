from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Short
from .forms import ShortUploadForm
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

@login_required
def upload_short(request):
    if request.method == 'POST':
        form = ShortUploadForm(request.POST, request.FILES)
        if form.is_valid():
            short = form.save(commit=False)
            short.author = request.user
            short.save()
            messages.success(request, "Шорт успешно загружен!")
            return redirect('shorts:feed')
    else:
        form = ShortUploadForm()

    return render(request, 'shorts/upload_short.html', {'form': form})

@login_required
def my_shorts(request):
    shorts = Short.objects.filter(author=request.user)
    return render(request, 'shorts/my_shorts.html', {'shorts': shorts})

@login_required
def edit_short(request, url_id):
    short = get_object_or_404(Short, url_id=url_id, author=request.user)

    if request.method == 'POST':
        form = ShortUploadForm(request.POST, instance=short)
        if form.is_valid():
            form.save()
            messages.success(request, "Шорт обновлен!")
            return redirect('shorts:shorts_mine')
    else:
        form = ShortUploadForm(instance=short)

    return render(request, 'shorts/edit_short.html', {'form': form, 'short': short})

@login_required
def delete_short(request, url_id):
    short = get_object_or_404(Short, url_id=url_id, author=request.user)
    if request.method == 'POST':
        short.delete()
        messages.success(request, "Шорт удалён.")
        return redirect('shorts:shorts_mine')
    return redirect('shorts:shorts_edit', url_id=url_id)