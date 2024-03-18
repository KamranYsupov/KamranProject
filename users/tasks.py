import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from kamranproject.celery import app
from .lists import quotes_list
from notifications.models import Notification

User = get_user_model()


@app.task
def send_mail_by_register(email):
    send_mail(
        'KamranProject',
        f"""
        Вы успешно прошли регистрацию на KamranProject!
        ______________________________________________
        Посетите другие наши сервисы:
            Новости KamranProject:
               {settings.PROJECT_URL}/list_of_pages/
            KamranVideo:
               {settings.PROJECT_URL}/KamranVideo/
            KamranGram:
               {settings.PROJECT_URL}/KamranGram/rooms/ 
               """,
        'kamranproject@yandex.ru',
        [email],
        fail_silently=False,
    )


@app.task
def send_random_quotes():
    list_of_emails = [i[0] for i in User.objects.filter(is_subscribed_on_quotes=True).values_list('email')]
    send_mail(
        'KamranQuotes',
        random.choice(quotes_list),
        'kamranproject@yandex.ru',
        list_of_emails,
        fail_silently=False
    )


@app.task
def send_weather_mail():
    list_of_emails = [i[0] for i in User.objects.filter(is_subscribed_on_weather=True).values_list('email')]
    send_mail(
        'KamranWeather🌥',
        """
         Понедельник: днём -4℃ | ночью -9℃'; ☁Пасмурно
         Вторник:     днём -4℃ | ночью -9℃'; ☁Пасмурно
         Среда:       днём -2℃ | ночью -7℃ ; ☁Пасмурно
         Четверг:     днём -3℃ | ночью -6℃ ; 🌨Небольшой снег
         Пятница:     днём -1℃ | ночью -5℃ ; ☁Пасмурно
         Суббота:     днём -0℃ | ночью -5℃ ; ☁Пасмурно
         Воскресенье: днём -0℃ | ночью -4℃ ; ☁Пасмурно
         """,
        'kamranproject@yandex.ru',
        list_of_emails,
        fail_silently=False
    )
