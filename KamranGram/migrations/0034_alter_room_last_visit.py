# Generated by Django 4.2.7 on 2024-02-17 05:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KamranGram', '0033_alter_room_last_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 17, 9, 39, 55, 233530), verbose_name='Последнее посещение'),
        ),
    ]
