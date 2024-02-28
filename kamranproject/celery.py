import os
import random

from celery import Celery
from celery.schedules import crontab

from users.lists import week_list, hour_list, minute_list

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KAMRkamranprojectAN.settings')

app = Celery('kamranproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weather_mail':{
        'task': 'users.tasks.send_weather_mail',
        'schedule': crontab(minute='45', hour='17', day_of_week='sunday'),
    },
    'send_random_quotes': {
        'task': 'users.tasks.send_random_quotes',
        'schedule': crontab(minute=random.choice(minute_list), hour=random.choice(hour_list), day_of_week=random.choice(week_list)),
    },
}
