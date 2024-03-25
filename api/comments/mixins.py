from django.conf import settings
from rest_framework import serializers

from comments.models import Comment


class ReplyMixinSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField(method_name='get_author_username')
    link = serializers.HyperlinkedIdentityField(
        view_name='api:read_comment',
        lookup_field='pk',
    )

    @staticmethod
    def get_likes(instance):
        return instance.likes.count()

    @staticmethod
    def get_parent(instance):
        if instance.parent:
            return f'{settings.PROJECT_URL}/api/v1/kamran-project/comments/{str(instance.parent.id)}/'

    @staticmethod
    def get_author_username(instance):
        if instance.author:
            return instance.author.username

    @staticmethod
    def get_video(instance):
        if instance.video:
            return f'{settings.PROJECT_URL}/api/v1/kamran-project/videos/watch/{str(instance.video.id)}/'

    @staticmethod
    def get_post(instance):
        if instance.post:
            return f'{settings.PROJECT_URL}/api/v1/kamran-project/articles/read/{str(instance.post.slug)}/'

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'comment',
            'likes',
            'time_create',
            'parent',
            'post',
            'video',
            'link'
        ]