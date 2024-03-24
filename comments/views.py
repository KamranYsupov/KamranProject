from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from notifications.models import Notification
from .forms import ReplyCommentForm
from .models import Comment

from notifications.tasks import send_notification, User

comments = (Comment.objects
            .select_related('author', 'post', 'parent', 'video')
            .prefetch_related('likes', 'replies__author', 'replies__likes'))


@login_required
def like_comment(request, object_id, comment_id, user_to_reply_id):
    url = settings.PROJECT_URL + request.POST.get('url_from')
    comment = comments.get(id=comment_id)
    liked_comments = comment.likes.filter(id=request.user.id)
    if liked_comments:
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    send_notification.delay(
        user_to_id=user_to_reply_id,
        user_from_id=request.user.id,
        event_type='Понравился комментарий',
        url=url
    )

    return redirect(url)


@login_required
def create_reply(request, parent_id, user_to_reply_id, is_reply_to_reply=False):
    url = settings.PROJECT_URL + request.POST.get('url_from')
    form = ReplyCommentForm(request.POST)
    if not form.is_valid():
        return redirect(settings.PROJECT_URL + request.POST.get('url_from'))

    user_to_reply = get_object_or_404(get_user_model(), id=int(user_to_reply_id))
    parent = get_object_or_404(Comment, id=int(parent_id))

    comment_text = form.cleaned_data.get('comment')

    Comment.objects.get_or_create(
        author=request.user,
        comment=comment_text,
        parent=parent,
        user_to_reply=user_to_reply,
        is_reply_to_reply=is_reply_to_reply,
    )

    send_notification(
        user_to_id=user_to_reply_id,
        user_from_id=request.user.id,
        event_type='Ответ на комментарий',
        text=comment_text,
    )

    return redirect(url)


def reply_comment(request, object_id, parent_id, user_to_reply_id):
    return create_reply(request, parent_id, user_to_reply_id)


def reply_to_reply(request, object_id, parent_id, user_to_reply_id):
    return create_reply(request, parent_id, user_to_reply_id, is_reply_to_reply=True)
