from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    MessageSerializer,
    RoomSerializer,
    DetailRoomSerializer,
    CreateRoomSerializer,
)

from KamranGram.models import Room, Message
from ..pagination import ObjectsListAPIPagination
from ..permissions import IsRoomCreatorOrReadOnly, IsSenderOrReadOnly
from ..users.serializers import UserSerializer

related_rooms = Room.objects.select_related('creator').prefetch_related('members', 'room_messages')


class EditMessageAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsSenderOrReadOnly, )


class RoomListAPIView(generics.ListAPIView):
    queryset = related_rooms
    serializer_class = RoomSerializer
    pagination_class = ObjectsListAPIPagination


class DetailRoomAPIView(generics.RetrieveAPIView):
    queryset = related_rooms
    serializer_class = DetailRoomSerializer
    permission_classes = (IsAuthenticated,)


class EditRoomAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = related_rooms
    serializer_class = CreateRoomSerializer
    permission_classes = (IsRoomCreatorOrReadOnly, )


class CreateRoomAPIView(generics.CreateAPIView):
    queryset = related_rooms
    serializer_class = CreateRoomSerializer
    permission_classes = (IsAuthenticated,)




