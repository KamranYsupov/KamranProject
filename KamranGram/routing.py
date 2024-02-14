from django.urls import re_path, path

from .consumers import KamranGramConsumer

websocket_urlpatterns = [
    path('ws/KGram/room/<room_id>/', KamranGramConsumer.as_asgi()),
]



