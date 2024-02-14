from django.conf import settings

from KamranGram.models import Room, Message
from api.users.serializers import UserSerializer
from api.users.views import UserAPIViewSet

from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    room_messages_count = serializers.SerializerMethodField()
    link = serializers.HyperlinkedIdentityField(
        view_name='api:room',
        lookup_field='pk'

    )

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'creator',
            'room_avatar',
            'theme',
            'members_count',
            'room_messages_count',
            'link',
        ]

    @staticmethod
    def get_creator(instance: Room):
        return str(instance.creator)

    @staticmethod
    def get_members_count(instance: Room):
        return instance.members.count()

    @staticmethod
    def get_room_messages_count(instance: Room):
        return instance.room_messages.count()


class MessageSerializer(serializers.ModelSerializer):
    time_send = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'content',
            'time_send',
            'room',
        ]

    @staticmethod
    def get_time_send(instance):
        return instance.time_send.strftime("%d-%m-%Y %H:%M:%S")

    @staticmethod
    def get_sender(instance):
        return str(instance.sender)

    @staticmethod
    def get_room(instance):
        if instance.room:
            return f'{settings.PROJECT_URL}/api/v1/kamran-project/KamranGram/room/{str(instance.room.id)}/'


class DetailRoomSerializer(RoomSerializer):
    members = UserSerializer(many=True)
    room_messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'creator',
            'room_avatar',
            'theme',
            'members',
            'room_messages',
            'members_count',
            'room_messages_count',
        ]


class CreateRoomSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    password = serializers.CharField(
        required=False,
        help_text='Если оставить поле "password" пустым, ваша комната будет открыта для всех',
        style={'input_type': 'password'}
    )

    class Meta:
        model = Room
        fields = ['name', 'description', 'theme', 'password', 'room_avatar', 'creator']
