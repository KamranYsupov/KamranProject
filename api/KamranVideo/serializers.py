from rest_framework import serializers

from KamranVideo.models import Video
from api.comments.serializers import CommentListSerializer
from api.mixins import BaseSerializerMixin

base_video_fields = [
    'id',
    'title',
    'video',
    'preview',
    'description',
    'views',
    'time_create',
    'author',
    'likes',
]


class VideoListSerializer(BaseSerializerMixin):
    comments_count = serializers.SerializerMethodField()
    watch_link = serializers.HyperlinkedIdentityField(
        view_name='api:watch',
        lookup_field='id',
        lookup_url_kwarg='video_id'
    )

    class Meta:
        model = Video
        fields = base_video_fields + ['comments_count', 'watch_link']

    @staticmethod
    def get_comments_count(instance):
        return instance.video_comments.count()


class WatchVideoSerializer(BaseSerializerMixin):
    video_comments = CommentListSerializer(many=True)

    class Meta:
        model = Video
        fields = base_video_fields + ['video_comments']


class CreateVideoSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Video
        fields = [
            'title',
            'video',
            'preview',
            'description',
            'author',
        ]
