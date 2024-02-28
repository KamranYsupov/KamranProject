from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView
from rest_framework.viewsets import ReadOnlyModelViewSet

from articles.models import Article
from articles.mixins import BaseMixin
from django.conf import settings
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, PasswordChangeUserForm

from .mixins import ChannelMixin, ArticlesChannelMixin
# from .serializers import UserSerializer
from .tasks import send_mail_by_register, send_random_quotes, send_weather_mail

User = get_user_model()


class LoginUser(BaseMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    title = 'Авторизация'


class RegisterUser(BaseMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    title = 'Регистрация'

    success_url = reverse_lazy('session_login')

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)


class ProfileUser(BaseMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')
    title = 'Мой профиль'

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChange(BaseMixin, PasswordChangeView):
    form_class = PasswordChangeUserForm
    template_name = 'users/password-change.html'
    success_url = reverse_lazy('profile')
    title = 'Изменение пароля'


class Channel(DetailView):
    model = get_user_model()
    context_object_name = 'owner'
    template_name = 'users/channel.html'
    pk_url_kwarg = 'owner_id'


class ArticlesChannel(ArticlesChannelMixin):
    template_name = 'users/channel_articles.html'
    order = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = (context['owner'].articles
                               .filter(is_published=True)
                               .prefetch_related('likes'))
        return context


class VideoChannel(ChannelMixin):
    template_name = 'users/channel_videos.html'
    order = 'videos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = context['owner'].videos.all()

        return context


class ArchiveChannel(ArticlesChannelMixin):
    template_name = 'users/channel_archive.html'
    order = 'archive'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archived_articles'] = (context['owner'].articles
                                        .filter(is_published=False)
                                        .prefetch_related('likes'))
        return context


def follow(request, owner_id):
    if owner_id == request.user.id:
        raise ValidationError('Вы не можете подписаться на себя')
    current_user = request.user
    owner_followers = get_user_model().objects.get(id=owner_id).followers
    if owner_followers.filter(id=current_user.id).exists():
        owner_followers.remove(current_user)
    else:
        owner_followers.add(current_user)

    return redirect(settings.PROJECT_URL + request.POST.get('url_from'))



