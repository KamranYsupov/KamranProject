from django import forms

from comments.models import Comment
from .models import Video


class AddVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video', 'preview', 'description']

        labels = {

        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'background: black;border-color: black',
                'rows': 1,
                'placeholder': 'Комментарий',
            }),
        }