from django.conf import settings
from rest_framework import serializers

from comments.models import Comment


class ReplySerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()
    comment_author = serializers.SerializerMethodField(method_name='get_comment_author_username')

    @staticmethod
    def get_likes(instance):
        return instance.likes.count()

    @staticmethod
    def get_parent(instance):
        if instance.parent:
            return f'{settings.PROJECT_URL}/api/v1/kamran-project/comments/{str(instance.parent.id)}/'

    @staticmethod
    def get_comment_author_username(instance):
        return instance.comment_author.username

    class Meta:
        model = Comment
        fields = [
            'id',
            'comment_author',
            'comment',
            'likes',
            'time_create',
            'parent',
        ]


class CommentDetailSerializer(ReplySerializer):
    comment_video = serializers.SerializerMethodField()
    comment_post = serializers.SerializerMethodField()
    replies = ReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'comment_author',
            'comment',
            'likes',
            'time_create',
            'comment_video',
            'comment_post',
            'parent',
            'replies',
        ]

    @staticmethod
    def get_comment_video(instance):
        if instance.comment_video:
            return f'{settings.PROJECT_URL}/api/v1/kamran-project/videos/watch/{str(instance.comment_video.id)}/'

    @staticmethod
    def get_comment_post(instance):
        if instance.comment_post:
            return f'{settings.PROJECT_URL}/api/v1/kamran-project/articles/read/{str(instance.comment_post.slug)}/'

    @staticmethod
    def get_parent(instance):
        if instance.parent:
            return {
                'id': instance.parent.id,
                'author': instance.parent.comment_author.username,
                'comment': instance.parent.comment,
                'likes': instance.likes.count(),
                'time_create': instance.parent.time_create,
                'link': f'{settings.PROJECT_URL}/api/v1/kamran-project/comments/{str(instance.parent.id)}/'

            }


class CommentSerializer(CommentDetailSerializer):
    link = serializers.HyperlinkedIdentityField(
        view_name='api:read_comment',
        lookup_field='pk'
    )
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'comment_author',
            'comment',
            'likes',
            'time_create',
            'comment_video',
            'comment_post',
            'parent',
            'replies_count',
            'link',
        ]

    @staticmethod
    def get_replies_count(instance):
        if instance.is_parent:
            return instance.replies.count()


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'comment',
            'comment_post',
        ]
