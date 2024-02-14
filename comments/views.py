from django.shortcuts import render, redirect
from django.conf import settings

from .forms import AddCommentForm
from .models import Comment

comments = (Comment.objects
            .select_related('author', 'post', 'parent', 'video')
            .prefetch_related('likes', 'replies__author', 'replies__likes'))


def like_comment(request, object_id, comment_id):
    comment = comments.get(id=comment_id)
    liked_comments = comment.likes.filter(id=request.user.id)
    if liked_comments:
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    return redirect(settings.PROJECT_URL + request.POST.get('url_from'))


def reply_comment(request, object_id, parent_id):
    parent_obj = comments.filter(id=parent_id).first()

    form = AddCommentForm(request.POST)
    if form.is_valid():
        Comment.objects.get_or_create(author=request.user,
                                      comment=form.cleaned_data.get('comment'),
                                      parent=parent_obj)

    return redirect(settings.PROJECT_URL + request.POST.get('url_from'))


