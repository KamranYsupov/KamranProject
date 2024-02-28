from django import forms

from KamranGram.models import Room
from users.forms import default_widget


class AddRoomForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль комнаты',
        required=False,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(
            attrs=default_widget | {'placeholder': '(не обязанельно)'}
        ))

    class Meta:
        model = Room
        fields = ['name', 'theme', 'room_avatar', 'password', 'limit_members', 'is_searchable', 'description']

        widgets = {
            'name': forms.TextInput(attrs=default_widget | {'placeholder': 'Название комнаты'}),
            'description': forms.Textarea(
                attrs=default_widget | {
                    'placeholder': '(необязанельно)',
                    'rows': 5,
                }),
            'theme': forms.Select(
                attrs=default_widget | {
                    'placeholder': 'Тема комнаты',
                    'style': 'background:#141214;color:white;width:100px;',
                }),
            'room_avatar': forms.FileInput(
                attrs=default_widget | {
                    'style': 'background:#141214;color:white;width:300px;'
                }),
            'limit_members': forms.NumberInput(
                attrs=default_widget | {
                    'placeholder': 'Лимит участников',
                    'style': 'background:#141214;color:white;width:66.5px;height:25px'}),
            'is_searchable': forms.CheckboxInput(
                attrs={
                    'placeholder': 'Доступна для поиска',
                    'class': 'form-check-input',
                }),
        }

        labels = {
            'room_avatar': 'Фото комнаты'
        }
