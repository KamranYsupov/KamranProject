from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Count, Prefetch, Q
from django import forms
from django.db.transaction import atomic

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, generics

from django.conf import settings

from kamranproject.service import like
from comments.service import deferred_comment_fields, prefetched_replies
from comments.views import comments
from notifications.tasks import send_notification
from .mixins import BaseMixin, ArticlesMixin
from .forms import AddPageForm, EditPageForm
from .models import Article

from comments.models import Comment
from comments.forms import AddCommentForm, ReplyCommentForm
from .service import deferred_article_fields

articles = (Article.objects.defer(*deferred_article_fields)
            .select_related('author').prefetch_related('likes')).filter(is_published=True)


def redirect_from_main_to_news(request):
    return redirect('articles_by_time')


class ArticlesByLikes(ArticlesMixin):
    queryset = articles_by_likes = articles.annotate(likes_count=Count('likes')).order_by('-likes_count')
    order = 'likes'


class ArticlesByLikePercent(ArticlesMixin):
    queryset = articles.order_by('-like_percent')
    order = 'like_percent'


class ArticlesByViews(ArticlesMixin):
    queryset = articles.order_by('-views')
    order = 'views'


class ArticlesByTime(ArticlesMixin):
    queryset = articles.order_by('-time_create')
    order = 'time'


class AddPage(BaseMixin, LoginRequiredMixin, CreateView):
    form_class = AddPageForm
    template_name = 'articles/add_page.html'
    success_url = reverse_lazy('articles_by_time')
    title = 'Добавление статьи'

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        return super().form_valid(form)


class EditPage(BaseMixin, LoginRequiredMixin, UpdateView):
    queryset = Article.objects.select_related('author').prefetch_related('likes')
    form_class = EditPageForm
    template_name = 'articles/edit-page.html'
    success_url = reverse_lazy('articles_by_time')
    slug_url_kwarg = 'edit_post_slug'
    title = 'Редактирование статьи'

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user != self.object.author and not user.is_superuser:
            raise PermissionError('Вы не можете редактировать чужую запись')
        return super().get_context_data(**kwargs)


class ShowPost(DetailView, BaseMixin, CreateView):
    queryset = Article.objects.select_related('author').prefetch_related('likes')
    form_class = AddCommentForm
    template_name = 'articles/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        article = kwargs['object']
        if self.request.user != article.author and self.request.user.is_authenticated:
            article.views += 1
            article.save()
        article_comments = (article.post_comments
                            .defer(*deferred_comment_fields)
                            .select_related('author', 'parent', 'user_to_reply')
                            .prefetch_related('likes',
                                              Prefetch('replies', queryset=Comment.objects
                                                       .select_related('author', 'parent', 'user_to_reply')
                                                       .prefetch_related('likes'),
                                                       ))
                            .annotate(likes_count=Count('likes'))
                            .order_by('-likes_count', '-time_create'))
        context = super().get_context_data(**kwargs)
        context['article_comments'] = article_comments
        context['reply_form'] = ReplyCommentForm
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('read', kwargs={'post_slug': self.kwargs['post_slug']})

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.post = self.get_object()
        return super().form_valid(form)


class ArticleSearch(BaseMixin, ListView):
    model = Article
    template_name = 'articles/list_of_pages.html'
    title = 'Новости'

    def get_context_data(self, *, object_list=None, **kwargs):
        article_search = self.request.GET.get('article_search')
        context = super().get_context_data(**kwargs)
        context['posts'] = (Article.objects
                            .select_related('author')
                            .prefetch_related('likes')
                            .filter(Q(is_published=True) &
                                    (Q(title__iregex=article_search) |
                                     Q(slug__iregex=article_search) |
                                     Q(content__iregex=article_search) |
                                     Q(author__username__iregex=article_search)))
                            )

        context['article_search'] = article_search
        context['title_by_query'] = f'"{article_search}" Поиск'
        return context


@login_required
def like_post(request, post_slug):
    article = articles.get(slug=post_slug)

    return like(request, article)
