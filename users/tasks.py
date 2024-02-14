import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from KAMRAN.celery import app
from .lists import quotes_list




@app.task
def send_mail_by_register(email):
    send_mail(
        'KamranProject',
        """
        Вы успешно прошли регистрацию на KamranProject!
        ______________________________________________
        Посетите другие наши сервисы:
            Новости KamranProject:
               127.0.0.1:8000/list_of_pages/
            KamranVideo:
               127.0.0.1:8000/KamranVideo/
            KamranGram:
               127.0.0.1:8000/KamranGram/rooms/ """,
        'kamranproject@yandex.ru',
        [email],
        fail_silently=False,
    )
    print(f'Письмо отправлено на почту {email}')


@app.task
def send_random_quotes():
    list_of_emails = [user.email for user in get_user_model().objects.filter(is_subscribed_on_quotes=True)]
    send_mail(
        'KamranQuotes',
        random.choice(quotes_list),
        'kamranproject@yandex.ru',
        list_of_emails,
        fail_silently=False
    )



@app.task
def send_weather_mail():
    list_of_emails = [user.email for user in get_user_model().objects.filter(is_subscribed_on_weather=True)]
    print(list_of_emails)
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