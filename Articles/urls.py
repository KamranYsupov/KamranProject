from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from Articles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainPage.as_view(), name='Articles'),
    path('articles/order=likes', views.ArticlesByLikes.as_view(), name='articles_by_likes'),
    path('articles/order=like_percent', views.ArticlesByLikePercent.as_view(), name='articles_by_like_percent'),
    path('articles/order=views', views.ArticlesByViews.as_view(), name='articles_by_views'),
    path('articles/order=new', views.ArticlesByTime.as_view(), name='articles_by_time'),
    path('add_page/', views.AddPage.as_view(), name='add_page'),
    path('read_post/<slug:post_slug>/', views.ShowPost.as_view(), name='read'),
    path('edit_post/<slug:edit_post_slug>/', views.EditPage.as_view(), name='edit-page'),
    path('like_post/<slug:post_slug>/', views.like_post, name='like_post'),
    path('search/', views.ArticleSearch.as_view(), name='article_search'),
]


