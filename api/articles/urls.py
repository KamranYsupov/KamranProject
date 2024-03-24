from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.articles import views
from api.articles import views


urlpatterns = [
    path('', views.ArticlesListAPIView.as_view(), name='articles_list'),
    path('create/', views.CreateArticleAPIView.as_view(), name='create_article'),
    path('read/<slug:post_slug>/', views.ReadArticleAPIView.as_view(), name='read_article'),
    path('edit/<slug:post_slug>/', views.EditArticleAPIView.as_view(), name='edit_article'),
]