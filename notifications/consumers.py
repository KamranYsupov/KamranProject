import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

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
        user_to = text_json_data['user_to']
        user_from = text_json_data['user_from']
        event_type = text_json_data['event_type']
        text = text_json_data['text']
        url = text_json_data['url']

        await self.save_notification(user_to, user_from, event_type, text=text, url=url)

        await self.channel_layer.group_send(
            self.user_to__id,
            {
                'type': 'send_notification',
                'user_to': user_to,
                'user_from': user_from,
                'event_type': event_type,
                'text': text,
                'url': url,
            }
        )

    async def send_notification(self, event):
        user_to = event['user_to']
        user_from = event['user_from']
        event_type = event['event_type']
        text = event['text']
        url = event['url']

        await self.send(
            text_data=json.dumps({
                'user_to': user_to,
                'user_from': user_from,
                'event_type': event_type,
                'text': text,
                'url': url,
            })
        )

    @sync_to_async
    def save_notification(self, user_to_id, user_from_id, event_type, text=None, url=None):
        user_to = get_user_model().objects.get(id=int(user_to_id))
        user_from = get_user_model().objects.get(id=int(user_from_id))

        Notification.objects.create(user_to=user_to, user_from=user_from, event_type=event_type, text=text, url=url)
