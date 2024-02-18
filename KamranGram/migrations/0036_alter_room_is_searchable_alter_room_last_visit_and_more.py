# Generated by Django 4.2.7 on 2024-02-17 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KamranGram', '0035_alter_room_last_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='is_searchable',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Доступна для поиска'),
        ),
        migrations.AlterField(
            model_name='room',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 17, 20, 18, 48, 82393), verbose_name='Последнее посещение'),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(db_index=True, max_length=20, unique=True, verbose_name='Название'),
        ),
    ]
