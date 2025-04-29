from django.urls import path
from . import views
 
app_name = 'shorts'
 
urlpatterns = [
    path('', views.shorts_feed, name='feed'),
    path('upload/', views.upload_short, name='shorts_upload'),
    path('mine/', views.my_shorts, name='shorts_mine'),
    path('edit/<str:url_id>/', views.edit_short, name='shorts_edit'),
    path('delete/<str:url_id>/', views.delete_short, name='shorts_delete'),
    path('<str:url_id>/like/', views.toggle_like, name='like'),
    path('<str:url_id>/', views.short_detail, name='detail'),
]