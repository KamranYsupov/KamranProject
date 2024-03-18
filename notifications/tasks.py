from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from kamranproject.celery import app
from .models import Notification


User = get_user_model()


@app.task
def send_notification(user_to_id, user_from, event_type, text=None, url=None):
    # if request.method == 'POST':

    user_to = get_object_or_404(User, id=int(user_to_id))
    # if user_to != user_from:
    Notification.objects.create(user_to=user_to, user_from=user_from, event_type=event_type, text=text, url=url)