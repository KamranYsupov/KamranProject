from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from users import my_models


class User(AbstractUser):
    followers = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True)
    avatar = my_models.AvatarImageField(
        upload_to='users/avatars/',
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'svg']
        )], default='users/avatars_default/default_avatar.png',
        verbose_name='Фото профиля')
    date_birth = models.DateField('Дата рождения', null=True)
    is_subscribed_on_quotes = models.BooleanField(
        'Подписка на рассылку цитат',
        default=False,
    )
    is_subscribed_on_weather = models.BooleanField(
        'Подписка на рассылку KamranWeather',
        default=False,
    )


