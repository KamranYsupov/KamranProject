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
                'id': 'add-comment-input',
                'class': 'form-control',
                'style': 'color:white;'
                         'height:10px;'
                         'width:700px;'
                         'margin:0;'
                         'background: #141214;'
                         'border-color:#141214;',
                'rows': 1,
                'placeholder': 'Комментарий',
            }),
        }
