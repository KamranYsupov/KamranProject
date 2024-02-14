from django.urls import path

from . import views

urlpatterns = [
    path('videos/', views.VideosAPIView.as_view()),
    path('create/', views.CreateVideoAPIView.as_view(), name='create_video'),
    path('watch/<int:video_id>/', views.WatchVideoAPIView.as_view(), name='watch'),
]



