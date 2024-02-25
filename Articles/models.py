from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from .tasks import set_like_percent

from KamranVideo.models import Video


class Article(models.Model):
    PUBLISHED = "Опубликованно"
    ARCHIVE = "Архив"

    IS_PUBLISHED = (
        (1, PUBLISHED),
        (0, ARCHIVE),
    )

    title = models.CharField(max_length=50, db_index=True, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, db_index=True, max_length=50, verbose_name='URL')
    content = models.TextField(verbose_name='Контент')
    photo = models.ImageField(upload_to='posts_images', verbose_name='Изображение', blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(choices=IS_PUBLISHED, default=PUBLISHED, verbose_name='Статус', db_index=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, default=0, null=True,
                               related_name='articles')
    likes = models.ManyToManyField(get_user_model(), related_name='posts_likes', blank=True)
    views = models.PositiveIntegerField(default=1)
    like_percent = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=100)], default=0)

    class Meta:
        ordering = ['-time_create']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__views = self.views

    def save(self, *args, **kwargs):
        if self.__views != self.views:
            set_like_percent.delay(self.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title



