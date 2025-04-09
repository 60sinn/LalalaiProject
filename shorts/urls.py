from django.urls import path
from . import views
 
app_name = 'shorts'
 
urlpatterns = [
    path('', views.shorts_feed, name='feed'),
    path('<str:url_id>/', views.short_detail, name='detail'),
]