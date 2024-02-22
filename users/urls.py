from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

channel_prefix = 'channel/<int:owner_id>/'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='session_login'),
    path('logout/', LogoutView.as_view(), name='session_logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password-change/', views.PasswordChange.as_view(), name='password-change'),
    path(channel_prefix + 'videos/', views.VideoChannel.as_view(), name='video-channel'),
    path(channel_prefix + 'articles/', views.ArticlesChannel.as_view(), name='articles-channel'),
    path(channel_prefix + 'articles/archive/', views.ArchiveChannel.as_view(), name='archive-channel'),
    path(channel_prefix + 'follow/', views.follow, name='follow'),
]
