# Generated by Django 5.0.1 on 2024-02-02 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KamranVideo', '0004_alter_video_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]