from django.contrib.auth import get_user_model
from django.db import models

from articles.models import Article
from KamranVideo.models import Video


class Comment(models.Model):
    comment = models.TextField(
        verbose_name='Комментарий',
        max_length=10000
    )
    time_create = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments',
        verbose_name='Автор',
    )
    post = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        related_name='post_comments',
        blank=True,
        verbose_name='Публикация',
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.SET_NULL,
        null=True,
        related_name='video_comments',
        blank=True,
        verbose_name='Видео',
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='replies',
        on_delete=models.CASCADE,
        verbose_name='Родительский коментарий'
    )
    user_to_reply = models.ForeignKey(
        get_user_model(),
        blank=True,
        null=True,
        related_name='answers',
        on_delete=models.SET_NULL,
        verbose_name='Ответ пользователю'
        )
    likes = models.ManyToManyField(
        get_user_model(),
        related_name='likes_comments',
        verbose_name='Лайки'
    )
    is_reply_to_reply = models.BooleanField(
        default=False,
        verbose_name='Является ли ответом на ответ'
    )

    class Meta:
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        if self.video:
            return f'{self.video.title[:20]} | {self.author}: {self.comment}'
        elif self.post:
            return f'{self.post.title[:20]} | {self.author}: {self.comment}'
        if self.parent:
            return (f'{self.author}: {self.comment[:30]}'
                    f' --reply to--> '
                    f'{self.parent.author}: {self.parent.comment[:30]}')
        return self.comment

    def get_reply_queryset(self):
        return (Comment.objects.
                select_related('author', 'post', 'video', 'parent')
                .filter(parent=self))

    @property
    def is_parent(self):
        return self.parent is None
