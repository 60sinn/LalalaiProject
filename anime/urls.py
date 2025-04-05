from django.urls import path
from . import views

urlpatterns = [
    path('', views.anime_list, name='anime_list'),  # Главная страница с аниме
    path('<str:anime_url_title>/', views.anime_detail, name='anime_detail'),  # Страница аниме
    path('<str:anime_url_title>/<str:season_url_title>/', views.season_detail, name='season_detail'), # Страница сезона
    path('<str:anime_url_title>/<str:season_url_title>/<str:episode_url_title>/', views.episode_detail, name='episode_detail'),  # Страница эпизода
]