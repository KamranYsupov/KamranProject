from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Notification

User = get_user_model()


def save_notification(user_to_id, user_from_id, event_type, post=None, video=None, text=None, url=None):
    user_to = get_object_or_404(User, id=int(user_to_id))
    user_from = get_object_or_404(User, id=int(user_from_id))

    Notification.objects.create(
        user_to=user_to,
        user_from=user_from,
        post=post,
        video=video,
        event_type=event_type,
        text=text,
        url=url
    )