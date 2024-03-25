from rest_framework import serializers

from articles.models import Article
from api.comments.serializers import CommentListSerializer
from api.mixins import BaseSerializerMixin

read_article_url = serializers.HyperlinkedIdentityField(
    view_name='api:read_article',
    lookup_url_kwarg='post_slug',
    lookup_field='slug',
)

base_fields = [
    'id',
    'title',
    'content',
    'slug',
    'photo',
    'time_create',
    'is_published',
    'author',
    'views',
    'likes',
    'like_percent',
]


class ArticleSerializerMixin(BaseSerializerMixin):
    read_url = read_article_url
    post_comments = CommentListSerializer(many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = base_fields

    @staticmethod
    def get_comments_count(instance):
        return instance.post_comments.count()


class ArticleCreateEditSerializerMixin(BaseSerializerMixin):
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
            'author'
        ]
