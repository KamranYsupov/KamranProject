from rest_framework import serializers

from articles.models import Article
from api.articles.mixins import (
    read_article_url,
    base_fields,
    ArticleSerializerMixin,
    ArticleCreateEditSerializerMixin
)


class ArticlesListSerializer(ArticleSerializerMixin):
    class Meta:
        model = Article
        fields = base_fields + ['post_comments_count', 'read_url']


class ReadArticleSerializer(ArticleSerializerMixin):
    class Meta:
        model = Article
        fields = base_fields + ['post_comments', 'post_comments_count']


class ArticleCreateSerializer(ArticleCreateEditSerializerMixin):
    link = read_article_url


class ArticleEditSerializer(ArticleCreateEditSerializerMixin):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'title',
            'slug',
            'content',
            'photo',
            'is_published',
            'author',
        ]
