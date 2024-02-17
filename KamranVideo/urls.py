from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from . import views


urlpatterns = [
    path('', views.Videos.as_view(), name='videos'),
    path('create_video/', views.CreateVideo.as_view(), name='create_video'),
    path('watch/video=<int:video_id>/', views.WatchVideo.as_view(), name='watch'),
    path('like_video/<int:video_id>/', views.like_video, name='like_video'),
    path('search/', views.VideoSearch.as_view(), name='video_search')

]
