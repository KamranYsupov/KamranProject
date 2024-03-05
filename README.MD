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

<h5 style='color:#5279c7'>Dockerfile</h5>

```Dockerfile
FROM python:3.10

COPY requirements.txt /temp/requirements.txt

WORKDIR /django_tree
EXPOSE 8000

RUN pip install psycopg2
RUN pip install -r /temp/requirements.txt
```

<h5 style='color:#5279c7'>docker-compose.yml</h5>

```yaml
services:
  django_tree:
    build:
      context: .
    ports:
      - '8000:8000'
    environment:
      - DB_HOST=database
      - DB_NAME=db_name
      - DB_USER=db_user
      - DB_PASS=db_pass
    volumes:
      - ./:/django_tree
    command: >
      sh -c "python manage.py runserver 0.0.0.0:8000"
    depends_on:
      - database

  database:
    image: postgres:14.6-alpine
    environment:
      - POSTGRES_DB=db_name
      - POSTGRES_USER=db_user
      - POSTGRES_PASSWORD=db_pass
      - POSTGRES_HOST_AUTH_METHOD=trust
```

<h5>Команды:</h5>

```commandline
docker-compose build
```

```commandline
docker-compose run --rm  django_tree sh -c "python manage.py makemigrations"
```

```commandline
docker-compose run --rm  django_tree sh -c "python manage.py migrate" 
```

```commandline
docker-compose run --rm  django_tree sh -c "python manage.py createsuperuser" 
```
```commandline
docker-compose up
```

<h3>Запуск на SQLite3</h4>

<h5>settings.py</h5>

```python
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

