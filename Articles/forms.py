from captcha.fields import CaptchaField
from django import forms

from .models import Article


class AddPageForm(forms.ModelForm):
   # captcha = CaptchaField(label="Введите текст с картинки")

    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'photo', 'is_published']

        labels = {
            'title': 'Заголовок:',
            'slug': 'URL:',
            'content': 'Контент:',
            'is_published': 'Статус:',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 3}),
        }


class EditPageForm(AddPageForm):
    slug = forms.SlugField(disabled=True, label='URL:')

    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'photo', 'is_published']

        labels = {
            'title': 'Заголовок:',
            'slug': 'URL:',
            'content': 'Контент:',
            'is_published': 'Статус:',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 20}),
        }
















