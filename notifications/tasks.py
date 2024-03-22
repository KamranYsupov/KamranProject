from asgiref.sync import async_to_sync, sync_to_async
from celery import shared_task
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from KamranVideo.models import Video
from articles.models import Article
from comments.models import Comment
from kamranproject.celery import app
from .models import Notification

User = get_user_model()


@shared_task
def send_notification(user_to_id, user_from_id, event_type,
                      post_id=None, video_id=None, comment_id=None, text=None, url=None):
    if user_to_id != user_from_id:
        user_to = get_object_or_404(User, id=int(user_to_id))
        user_from = get_object_or_404(User, id=int(user_from_id))

        post = get_object_or_404(Article, id=int(post_id)) if post_id is not None else None
        video = get_object_or_404(Video, id=int(video_id)) if video_id is not None else None
        comment = get_object_or_404(Comment, id=int(comment_id)) if comment_id is not None else None

        Notification.objects.create(
            user_to=user_to,
            user_from=user_from,
            post=post,
            video=video,
            comment=comment,
            event_type=event_type,
            text=text,
            url=url
        )
        #
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     str(user_to_id),
        #     {
        #         'type': 'send_notification',
        #         'user_to_id': str(user_to_id),
        #         'user_from_id': str(user_from_id),
        #         'user_from_username': user_from.username,
        #         'user_from_avatar': user_from.avatar,
        #         'post_id': str(post_id),
        #         'post_title': post.title if post is not None else None,
        #         'video_id': str(video_id),
        #         'video_title': video.title if video is not None else None,
        #         'event_type': event_type,
        #         'text': text,
        #         'url': url,
        #     }
        # )
