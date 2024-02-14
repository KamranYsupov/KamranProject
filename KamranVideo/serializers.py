from django.contrib.auth import get_user_model
from rest_framework import serializers

from KamranVideo.models import Video


# from users.serializers import UserSerializer


class VideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_video(self, instance) -> object:
        return str(instance.video)

    def get_preview(self, instance) -> object:
        return str(instance.preview)

    def get_author(self, instance) -> dict:
        return {
            'id': instance.author.id,
            'username': instance.author.username,
            'E-mail': instance.author.email,
        }

    def get_likes(self, instance) -> object:
        return int(instance.likes.count())

    class Meta:
        model = Video
        fields = ['id', 'title', 'video', 'preview', 'likes', 'description', 'author']
