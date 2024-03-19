import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from KamranVideo.models import Video
from articles.models import Article
from notifications.models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_to__id = self.scope['url_route']['kwargs']['user_to__id']

        await self.channel_layer.group_add(
            self.user_to__id,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.user_to__id,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_json_data = json.loads(text_data)
        user_to_id = text_json_data['user_to_id']
        user_from_id = text_json_data['user_from_id']
        user_from_username = text_json_data['user_from_username']
        user_from_avatar = text_json_data['user_from_avatar']
        post_id = text_json_data['post_id']
        post_title = text_json_data['post_title']
        video_id = text_json_data['video_id']
        video_name = text_json_data['video_name']
        event_type = text_json_data['event_type']
        text = text_json_data['text']
        url = text_json_data['url']

        await self.save_notification(text_json_data)

        await self.channel_layer.group_send(
            self.user_to__id,
            {
                'type': 'send_notification',
                'user_to_id': user_to_id,
                'user_from_id': user_from_id,
                'user_from_username': user_from_username,
                'user_from_avatar': user_from_avatar,
                'post_id': post_id,
                'post_title': post_title,
                'video_id': video_id,
                'video_name': video_name,
                'event_type': event_type,
                'text': text,
                'url': url,
            }
        )

    async def send_notification(self, event):
        user_to_id = event['user_to_id']
        user_from_id = event['user_from_id']
        user_from_username = event['user_from_username']
        user_from_avatar = event['user_from_avatar']
        post_id = event['post_id']
        post_title = event['post_title']
        video_id = event['video_id']
        video_name = event['video_name']
        event_type = event['event_type']
        text = event['text']
        url = event['url']

        await self.send(
            text_data=json.dumps({
                'user_to_id': user_to_id,
                'user_from_id': user_from_id,
                'user_from_username': user_from_username,
                'user_from_avatar': user_from_avatar,
                'post_id': post_id,
                'post_title': post_title,
                'video_id': video_id,
                'video_name': video_name,
                'event_type': event_type,
                'text': text,
                'url': url,
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
