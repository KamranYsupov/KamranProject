from django.contrib.auth import get_user_model
from django.db import models

from KamranVideo.models import Video
from articles.models import Article
from comments.models import Comment

User = get_user_model()


class Notification(models.Model):
    EVENT_TYPES = [
        ('from_administration', 'От администрации'),
        ('comment_post', 'Комментирование статьи'),
        ('comment_video', 'Комментирование видео'),
        ('like_comment', 'Понравился комментарий'),
        ('reply_comment', 'Ответ на комментарий'),
        ('like_post', 'Понравилась статья'),
        ('like_video', 'Понравилось видео'),
        ('follow', 'Подписка'),
    ]

    user_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Получатель',
    )
    user_from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='От кого',
        blank=True,
        null=True,
    )
    post = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='Статья',
        blank=True,
        null=True,
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        verbose_name='Видео',
        blank=True,
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        verbose_name='Комментарий',
        blank=True,
        null=True,
    )
    event_type = models.CharField(verbose_name='Тип события', max_length=40, choices=EVENT_TYPES)
    text = models.TextField(verbose_name='Текст', blank=True, null=True)
    url = models.URLField(verbose_name='Ссылка', blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')
    is_watched = models.BooleanField(default=False, verbose_name='Просмотренно')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-time_create']
