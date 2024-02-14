import json
import os

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from users.models import User
from .models import Room, Message


class KamranGramConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = int(self.scope['url_route']['kwargs']['room_id'])
        self.room_group_name = f'room_{self.room_id}'
        print(self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        avatar = text_data_json['avatar']
        room_id = text_data_json['room_id']

        await self.save_message(message, sender, room_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message,
                'sender': sender,
                'avatar': avatar,
                'room_id': room_id,
            }
        )

    async def send_message(self, event):
        message = event['message']
        sender = event['sender']
        avatar = event['avatar']
        await self.send(text_data=json.dumps({'message': message, 'sender': sender, 'avatar': avatar}))

    @sync_to_async
    def save_message(self, message, username, room_id):
        print(username, room_id, "----------------------", message)
        sender = get_user_model().objects.get(username=username)
        room = Room.objects.get(id=room_id)

        Message.objects.create(sender=sender, room=room, content=message)

