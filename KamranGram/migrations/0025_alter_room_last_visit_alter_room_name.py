# Generated by Django 4.2.7 on 2024-02-13 02:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KamranGram', '0024_alter_room_last_visit_alter_room_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 13, 6, 15, 33, 905159)),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]