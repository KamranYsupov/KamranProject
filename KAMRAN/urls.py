from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Articles.urls')),
    path('users/', include('users.urls')),
    path('captcha/', include('captcha.urls')),
    path('KamranVideo/', include('KamranVideo.urls')),
    path('KamranGram/', include('KamranGram.urls')),
    path('comments/', include('comments.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    # API
    path('api/v1/kamran-project/', include('api.urls', namespace='api')),
    path('api/v1/session_auth/', include('rest_framework.urls')),
    path('api/v1/djoser_auth/', include('djoser.urls')),
    re_path('^djoser_auth/', include('djoser.urls.authtoken')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
