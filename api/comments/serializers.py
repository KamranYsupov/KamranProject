from django.conf import settings
from rest_framework import serializers

from .mixins import ReplyMixinSerializer
from comments.models import Comment


class CommentDetailSerializer(ReplyMixinSerializer):
    replies = ReplyMixinSerializer(many=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'comment',
            'likes',
            'time_create',
            'video',
            'post',
            'parent',
            'replies',
        ]

    @staticmethod
    def get_parent(instance):
        if instance.parent:
            return {
                'id': instance.parent.id,
                'author': instance.parent.author.username,
                'comment': instance.parent.comment,
                'likes': instance.likes.count(),
                'time_create': instance.parent.time_create,
                'link': f'{settings.PROJECT_URL}/api/v1/kamran-project/comments/{str(instance.parent.id)}/'

            }


class CommentSerializer(ReplyMixinSerializer):
    link = serializers.HyperlinkedIdentityField(
        view_name='api:read_comment',
        lookup_field='pk'
    )
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'comment',
            'likes',
            'time_create',
            'video',
            'post',
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
            'post',
            'video',
            'parent',
            'user_to_reply',
            'is_reply_to_reply',
        ]
