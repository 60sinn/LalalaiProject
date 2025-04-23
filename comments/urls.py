from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    # шортики
    path('shorts/<str:short_id>/comments/', views.get_short_comments, name='get_short_comments'),
    path('shorts/<str:short_id>/comments/post/', views.post_short_comment, name='post_short_comment'),

    # анимешки
    path('anime/<slug:slug>/comments/', views.get_anime_comments, name='get_anime_comments'),
    path('anime/<slug:slug>/comments/post/', views.post_anime_comment, name='post_anime_comment'),

    # сезончики
    path('season/<slug:season_slug>/comments/', views.get_season_comments, name='get_season_comments'),
    path('season/<slug:season_slug>/comments/post/', views.post_season_comment, name='post_season_comment'),

    # эпизоДИКИ)
    path('episode/<slug:episode_slug>/comments/', views.get_episode_comments, name='get_episode_comments'),
    path('episode/<slug:episode_slug>/comments/post/', views.post_episode_comment, name='post_episode_comment'),
]