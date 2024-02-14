from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import VideoListSerializer, WatchVideoSerializer, CreateVideoSerializer

from KamranVideo.models import Video
from comments.service import video_comments_prefetch
from ..pagination import ObjectsListAPIPagination

videos = Video.objects.select_related('author').prefetch_related('likes', video_comments_prefetch)

prefetch_videos = Video.objects.select_related('author').prefetch_related('likes', 'video_comments')


class VideosAPIView(generics.ListAPIView):
    queryset = prefetch_videos
    serializer_class = VideoListSerializer
    pagination_class = ObjectsListAPIPagination


class WatchVideoAPIView(generics.RetrieveAPIView):
    queryset = videos
    serializer_class = WatchVideoSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'video_id'


class CreateVideoAPIView(generics.CreateAPIView):
    queryset = videos
    serializer_class = CreateVideoSerializer
    permission_classes = (IsAuthenticated,)
