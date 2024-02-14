from rest_framework import serializers

from Articles.models import Article
from api.Articles.mixins import read_article_url, base_fields, ArticleSerializerMixin


class ArticlesListSerializer(ArticleSerializerMixin):
    class Meta:
        model = Article
        fields = base_fields + ['post_comments_count', 'read_url']


class ReadArticleSerializer(ArticleSerializerMixin):
    class Meta:
        model = Article
        fields = base_fields + ['post_comments', 'post_comments_count']


class ArticleCreateSerializer(serializers.ModelSerializer):
    link = read_article_url
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = [
            'title',
            'slug',
            'content',
            'photo',
            'is_published',
            'link',
            'author']


class ArticleEditSerializer(ArticleCreateSerializer):
    slug = serializers.SlugField(read_only=True)
