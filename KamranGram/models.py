import datetime
import os

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from KAMRAN import settings
from users import my_models


class Room(models.Model):
    BLUE = 'Голубая'
    RED = 'Красная'
    DARK = 'Темная'
    LIGHT = 'Светлая'
    GREEN = 'Зеленая'
    PURPLE = 'Фиолетовая'

    THEME_CHOICES = [
        ('#1bc3e0', BLUE),
        ('#cc1d1f', RED),
        ('#141214', DARK),
        ('#06d606', GREEN),
        ('#ab09e0', PURPLE),
    ]

    name = models.CharField(verbose_name='Название', db_index=True, max_length=20, unique=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='rooms',
                                verbose_name='Создатель')
    members = models.ManyToManyField(get_user_model(), related_name='current_rooms', verbose_name='Участники')
    description = models.TextField(verbose_name='Описание', max_length=300, blank=True)
    theme = models.CharField(verbose_name='Тема', max_length=20, choices=THEME_CHOICES, default=BLUE)
    time_create = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    password = models.CharField(verbose_name='Пароль комнаты', max_length=20, blank=True)
    limit_members = models.PositiveIntegerField(verbose_name='Лимит участников', default=2)
    is_searchable = models.BooleanField(verbose_name='Доступна для поиска', db_index=True, default=True)
    room_avatar = my_models.AvatarImageField(
        upload_to='KamranGram/room_avatars',
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'svg']
        )],
        default='KamranGram/room_avatars/default_group.png'
    )

    class Meta:
        ordering = ['-time_create']
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return self.name


class Message(models.Model):
    content = models.TextField(max_length=200)
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_messages')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='room_messages')
    time_send = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time_send']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.content
        # if len(str(self.content)) > 15:
        #    return f'{self.sender}: {self.content[:15]}..'
        # return f'{self.sender}: {self.content}'
