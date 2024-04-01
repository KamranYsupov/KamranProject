<h3>Новости</h3>
<img src="media\README_images\articels-for-github.png" style="margin:0">
<h3>Видеохостинг</h3>
<img src="media\README_images\videos-for-github.png" style="margin:0">
<img src="media\README_images\comment-replies-for-github.png"/>
<h3>Мессенджер</h3>
<img src="media\README_images\room-for-github.png" style="margin:0">
<img src="media\README_images\room-settings-for-github.png" style="margin:0">
<h3>Личный канал</h3>
<img src="media\README_images\channel-articles-for-github.png" style="margin:0">
<img src="media\README_images\channel-videos-for-github.png" style="margin:0">


<h2>Setup</h2>

<h3>Настройка venv</h3>

<h4>Windows</h4>

```commandline
python -m venv <virtualenv name>
```

<h4>Ubuntu</h4>

```commandline
python3 -m venv <virtualenv name>
```

<h4>Windows</h4>

```commandline
./<virtualenv name>/Scripts/activate
```

<h4>Ubuntu</h4>

```commandline
source /<virtualenv name>/bin/activate
```
<br>
<br>

```commandline
pip install -r requirements.txt
```

<h3>Запуск на PostgreSQL</h3>

<h5>settings.py</h5>

```python
# POSTGRES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}
```

<h5>Команды:</h5>

```commandline
docker-compose build
```

```commandline
docker-compose run --rm  web-app sh -c "python manage.py makemigrations"
```

```commandline
docker-compose run --rm  web-app sh -c "python manage.py migrate" 
```

```commandline
docker-compose run --rm  web-app sh -c "python manage.py createsuperuser" 
```
```commandline
docker-compose up
```

<h3>Запуск на SQLite3</h4>

<h5>settings.py</h5>

```python
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'captcha',
    'djoser',
    'debug_toolbar',
    'social_django',
   # 'cachalot', Если не закоментировать cachalot, то будет ошибка Error 11001 connecting to redis:6379. getaddrinfo failed.

    'articles',
    'KamranGram',
    'KamranVideo',
    'notifications',
    'comments',
    'users',
    'api',

]

# SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

<h5>Команды:</h5>

```commandline
python manage.py makemigrations
```

```commandline
python manage.py migrate
```

```commandline
python manage.py createsuperuser
```

```commandline
python manage.py runserver
```

