from django import forms
from .models import Comment


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
                         'width:800px;'
                         'margin:0;'
                         'background: #141214;'
                         'border-color:#141214;',
                'minlength': 1,
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
                'style': 'height:20px;color:white;width:100px;margin:0;background: #141214;border-color:gray',
                'placeholder': 'Ответ на комментарий',
            }),
        }
