from django import forms

from comments.models import Comment
from users.forms import default_widget
from .models import Video


class AddVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video', 'preview', 'description']

        widgets = {
            'title': forms.TextInput(attrs=default_widget | {'placeholder': 'Название видео'}),
            'video': forms.FileInput(
                attrs=default_widget | {'placeholder': 'Видео'}),
            'preview': forms.FileInput(
                attrs=default_widget | {'placeholder': 'Превью'}),
            'description': forms.Textarea(
                attrs=default_widget | {'placeholder': 'Описание видео(необязательно)'}),
        }
        labels = {
            'title': 'Название',
            'video': 'Видео',
            'preview': 'Превью',
            'description': 'Описание видео',
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'background: black;border-color: black;color:white;',
                'rows': 1,
                'placeholder': 'Комментарий',
            }),
        }
