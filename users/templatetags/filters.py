from django import template
from django import forms

register = template.Library()


@register.filter
def date_format(date, format='%Y-%m-%d'):
    try:
        return date.strftime(format)
    except AttributeError:
        raise forms.ValidationError('Некорректный формат файла')
