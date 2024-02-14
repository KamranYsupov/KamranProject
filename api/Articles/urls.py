from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.Articles import views
from api.Articles import views


urlpatterns = [
    path('', views.ArticlesListAPIView.as_view()),
    path('create/', views.CreateArticleAPIView.as_view(), name='create_article'),
    path('read/<slug:post_slug>/', views.ReadArticleAPIView.as_view(), name='read_article'),
    path('edit/<slug:post_slug>/', views.EditArticleAPIView.as_view(), name='edit_article'),
]