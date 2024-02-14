from django import forms
from django.conf import settings
from django.shortcuts import redirect


def like(request, obj):
    if obj.author == request.user:
        raise forms.ValidationError('Вы не можете поставить лайк под свою публикацию')
    liked_list = obj.likes.filter(id=request.user.id)
    if liked_list:
        obj.likes.remove(request.user)
    else:
        obj.likes.add(request.user)

    return redirect(settings.PROJECT_URL + request.POST.get('url_from'))
