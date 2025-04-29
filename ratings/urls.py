from django.urls import path
from .views import rate_anime, rate_season

urlpatterns = [
    path('rate/', rate_anime, name='rate_anime'),
    path('rate-season/', rate_season, name='rate_season'),
]
