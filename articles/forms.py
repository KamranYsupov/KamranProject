from django import forms

from users.forms import default_widget
from .models import Article


class AddPageForm(forms.ModelForm):

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
            'title': forms.TextInput(attrs=default_widget | {'placeholder': 'Заголовок'}),
            'slug': forms.TextInput(attrs=default_widget | {'placeholder': 'URL'}),
            'content': forms.Textarea(
                attrs=default_widget |
                      {
                          'placeholder': 'Контент(не обязательно):',
                          'cols': 40,
                          'rows': 3
                      }
            ),
            'photo': forms.FileInput(attrs=default_widget | {'class': 'form-control-sm'}),
            'is_published': forms.Select(attrs=default_widget | {'class': 'form-control-sm'}),
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
