from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

app_name = 'api'

urlpatterns = [
    path('articles/', include('api.articles.urls')),
    path('comments/', include('api.comments.urls')),
    path('KamranVideo/', include('api.KamranVideo.urls')),
    path('KamranGram/', include('api.KamranGram.urls')),
    path('', include('api.users.urls')),
]
