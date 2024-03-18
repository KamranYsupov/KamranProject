from django.urls import path

from KamranGram.consumers import KamranGramConsumer
from notifications.consumers import NotificationConsumer


websocket_urlpatterns = [
    path('ws/KGram/room/<room_id>/', KamranGramConsumer.as_asgi()),
    path('ws/notifications/<user_to__id>/', NotificationConsumer.as_asgi()),
]