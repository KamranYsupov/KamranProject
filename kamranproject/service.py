from django import forms
from django.conf import settings
from django.shortcuts import redirect

from notifications.tasks import send_notification


def is_connection_by_websocket(url: str) -> bool:
    """Проверяем был ли запрос по url адресу через websocket"""
    return url.__contains__('read_post') or url.__contains__('watch')


def object_checker(obj):
    """Проверяем с обьектом какой модели работаем(Article или Video)"""
    try:
        slug = obj.slug
        result = 'Article'

    except AttributeError:
        result = 'Video'

    return result


def get_event_type(obj):
    if object_checker(obj) == 'Article':
        event_type = 'Понравилась статья'
    else:
        event_type = 'Понравилось видео'

    return event_type


def like(request, obj):
    if obj.author == request.user:
        raise forms.ValidationError('Вы не можете поставить лайк под свою публикацию')

    url = settings.PROJECT_URL + request.POST.get('url_from')
    liked_list = obj.likes.filter(id=request.user.id)

    if liked_list:
        obj.likes.remove(request.user)
    else:
        obj.likes.add(request.user)
        obj.views += 1
        obj.save()

        if not is_connection_by_websocket(url):
            send_notification.delay(
                user_to_id=int(request.POST.get('user_to_id')),
                user_from_id=request.user.id,
                event_type=get_event_type(obj),
                url=url
            )

    return redirect(url)
