from django.db.models import Q, Prefetch
from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from Articles.models import Article

from api.Articles.serializers import (
    ArticlesListSerializer,
    ArticleEditSerializer,
    ArticleCreateSerializer,
    ReadArticleSerializer,
)
from comments.service import post_comments_prefetch

from api.pagination import ObjectsListAPIPagination
from api.permissions import IsOwnerOrReadOnly
from comments.models import Comment

articles = Article.objects.select_related('author').prefetch_related('likes', post_comments_prefetch)

prefetch_articles = Article.objects.select_related('author').prefetch_related('likes', 'post_comments')


class ArticlesListAPIView(generics.ListAPIView):
    serializer_class = ArticlesListSerializer
    pagination_class = ObjectsListAPIPagination

    def get_queryset(self):
        queryset_list = prefetch_articles
        query = self.request.GET.get('articles_search')
        if query:
            queryset_list = prefetch_articles.filter(
                Q(title__iregex=query) |
                Q(content__iregex=query) |
                Q(slug__iregex=query) |
                Q(author__username__iregex=query) |
                Q(author__first_name__iregex=query) |
                Q(author__last_name__iregex=query)
            )
        return queryset_list


class CreateArticleAPIView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = (IsAuthenticated,)


class ReadArticleAPIView(generics.RetrieveAPIView):
    queryset = articles
    serializer_class = ReadArticleSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'


class EditArticleAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = articles
    serializer_class = ArticleEditSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'
