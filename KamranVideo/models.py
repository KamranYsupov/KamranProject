import datetime

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from . import my_models


class Video(models.Model):
    video = my_models.VideoField(upload_to='KamranVideo/videos',
                                 validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    preview = my_models.LimitedImageField(upload_to='KamranVideo/previews',
                                          validators=[FileExtensionValidator(
                                              allowed_extensions=['jpg', 'jpeg', 'png', 'svg']
                                          )],
                                          help_text='Поддерживаются изображения в формате: 1280 ✕ 720, 1366 ✕ 768, '
                                                    '1920 ✕ 1080')
    description = models.TextField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    author = models.ForeignKey(get_user_model(), related_name='videos', on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(get_user_model(), related_name='video_likes', blank=True)
    views = models.PositiveIntegerField(default=1)
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.title


