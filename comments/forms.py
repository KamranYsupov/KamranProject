from django import forms
from .models import Comment


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height:10px;width:800px;margin:0;background: #141214;border-color: #141214',
                'rows': 1,
                'placeholder': 'Комментарий',
            }),
        }


class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height:10px;width:500px;margin:0;background: #141214;border-color: #141214;',
                'placeholder': 'Ответ на комментарий',
            }),
        }
