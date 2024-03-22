import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from KamranVideo.models import Video
from articles.models import Article
from notifications.models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_to_id = self.scope['url_route']['kwargs']['user_to__id']

        await self.channel_layer.group_add(
            self.user_to_id,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.user_to_id,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_json_data = json.loads(text_data)
        user_to_id = text_json_data.get('user_to_id')
        user_from_id = text_json_data.get('user_from_id')
        user_from_username = text_json_data.get('user_from_username')
        user_from_avatar = text_json_data.get('user_from_avatar')
        post_id = text_json_data.get('post_id')
        post_title = text_json_data.get('post_title')
        video_id = text_json_data.get('video_id')
        video_title = text_json_data.get('video_title')
        event_type = text_json_data.get('event_type')
        text = text_json_data.get('text')
        url = text_json_data.get('url')
        is_watched = text_json_data.get('is_watched')

        if is_watched:
            return await self.set_notifications_status_watched(text_json_data)

        await self.save_notification(text_json_data)

        await self.channel_layer.group_send(
            self.user_to_id,
            {
                'type': 'send_notification',
                'user_to_id': user_to_id,
                'user_from_id': user_from_id,
                'user_from_username': user_from_username,
                'user_from_avatar': user_from_avatar,
                'post_id': post_id,
                'post_title': post_title,
                'video_id': video_id,
                'video_title': video_title,
                'event_type': event_type,
                'text': text,
                'url': url,
                'is_watched': is_watched,
            }
        )

    async def send_notification(self, event):
        await self.send(
            text_data=json.dumps({
                'user_to_id': event.get('user_to_id'),
                'user_from_id': event.get('user_from_id'),
                'user_from_username': event.get('user_from_username'),
                'user_from_avatar': event.get('user_from_avatar'),
                'post_id': event.get('post_id'),
                'post_title': event.get('post_title'),
                'video_id': event.get('video_id'),
                'video_title': event.get('video_title'),
                'event_type': event.get('event_type'),
                'text': event.get('text'),
                'url': event.get('url'),
            })
        )

    @sync_to_async
    def save_notification(self, data):
        user_to = get_user_model().objects.get(id=int(data['user_to_id']))
        user_from = get_user_model().objects.get(id=int(data['user_from_id']))

        if data['post_id'] is not None:
            data['post_id'] = Article.objects.get(id=int(data['post_id']))
        if data['video_id'] is not None:
            data['video_id'] = Video.objects.get(id=int(data['video_id']))

        Notification.objects.create(
            user_to=user_to,
            user_from=user_from,
            event_type=data['event_type'],
            post=data['post_id'],
            video=data['video_id'],
            text=data['text'],
            url=data['url'],
        )

    @sync_to_async
    def set_notifications_status_watched(self, data):
        user = get_user_model().objects.get(id=int(data['user_to_id']))
        user.notifications.all().update(is_watched=True)





