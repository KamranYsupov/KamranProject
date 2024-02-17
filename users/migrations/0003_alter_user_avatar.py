# Generated by Django 4.2.7 on 2024-02-17 05:39

import django.core.validators
from django.db import migrations
import users.my_models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=users.my_models.AvatarImageField(default='users/avatars_default/nursultan.jpeg', upload_to='users/avatars/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]),
        ),
    ]