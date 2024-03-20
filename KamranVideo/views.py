from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView
from rest_framework.viewsets import ReadOnlyModelViewSet

from articles.views import comments
from django.conf import settings
from articles.mixins import BaseMixin
from kamranproject.service import like
from comments.forms import ReplyCommentForm
from comments.service import deferred_comment_fields
from notifications.tasks import send_notification
from comments.forms import AddCommentForm
from .forms import AddVideoForm
from .models import Video
from .serializers import VideoSerializer

related_video_queryset = Video.objects.select_related('author').prefetch_related('likes')


class Videos(BaseMixin, ListView):
    queryset = Video.objects.select_related('author')
    context_object_name = 'videos'
    template_name = 'KamranVideo/videos.html'
    title = 'KamranVideo'


class CreateVideo(BaseMixin, CreateView):
    form_class = AddVideoForm
    template_name = 'KamranVideo/create_video.html'
    success_url = reverse_lazy('videos')
    title = 'Создать видео'

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        return super().form_valid(form)


class WatchVideo(DetailView, BaseMixin, CreateView):
    queryset = related_video_queryset
    form_class = AddCommentForm
    template_name = 'KamranVideo/watch.html'
    context_object_name = 'video'
    pk_url_kwarg = 'video_id'
    title = 'Просмотр видео'

    def get_context_data(self, **kwargs):
        video = kwargs['object']
        if self.request.user != video.author:
            video.views += 1
            video.save()

        video_comments = (video
                          .video_comments.defer(*deferred_comment_fields)
                          .select_related('author')
                          .prefetch_related('likes', 'replies__likes', 'replies__author')
                          .annotate(likes_count=Count('likes'))
                          .order_by('-likes_count'))

        context = super().get_context_data(**kwargs)
        context['videos'] = related_video_queryset
        context['video_comments'] = video_comments
        context['reply_form'] = ReplyCommentForm
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('watch', kwargs={'video_id': self.kwargs['video_id']})

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.video = self.get_object()
        return super().form_valid(form)


class VideoSearch(BaseMixin, ListView):
    model = Video
    template_name = 'KamranVideo/videos.html'
    title = 'KamranVideo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        video_search = self.request.GET.get('video_search')
        context['videos'] = (Video.objects
                             .select_related('author')
                             .filter(Q(title__iregex=video_search)
                                     | Q(author__username__iregex=video_search)))
        context['video_search'] = video_search

        return context


@login_required
def like_video(request, video_id):
    video = Video.objects.get(id=video_id)

    return like(request, video)