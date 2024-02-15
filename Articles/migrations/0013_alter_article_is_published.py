# Generated by Django 5.0.1 on 2024-02-06 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Articles', '0012_alter_article_content_alter_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_published',
            field=models.BooleanField(choices=[(1, 'Опубликованно'), (0, 'Архив')], db_index=True, default='Опубликованно', verbose_name='Статус'),
        ),
    ]