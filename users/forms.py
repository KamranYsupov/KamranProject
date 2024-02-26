import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

current_year = datetime.date.today().year
default_widget = {
    'class': 'form-control',
    'style': 'color: white;background: #141214;border-color: #141214;',
}


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs=default_widget | {'placeholder': 'Имя пользователя'}))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs=default_widget | {'placeholder': 'Пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', max_length=50, min_length=3,
                               widget=forms.TextInput(
                                   attrs=default_widget | {'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='E-mail', required=True,
                             widget=forms.EmailInput(
                                 attrs=default_widget | {'placeholder': 'name@example.com'}))

    password1 = forms.CharField(label='Пароль', max_length=20, min_length=6,
                                widget=forms.PasswordInput(
                                    attrs=default_widget | {'placeholder': 'Пароль'}))

    password2 = forms.CharField(label='Повторение пароля', max_length=20, min_length=6,
                                widget=forms.PasswordInput(
                                    attrs=default_widget | {'placeholder': 'Повторение пароля'}))

    date_birth = forms.DateField(label='Дата рождения',
                                 widget=forms.DateInput(
                                     attrs={
                                         'type': 'date',
                                         'class': 'form-control',
                                         'style':
                                             'margin-top:5px;'
                                             'background: #141214;'
                                             'border-color: #141214;'
                                             'color:white;',
                                         'placeholder': 'Дата рождения'
                                     }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar', 'date_birth', 'password1', 'password2',
                  'is_subscribed_on_quotes', 'is_subscribed_on_weather']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

        widgets = {
            'avatar': forms.FileInput(attrs=default_widget | {'class': 'form-control-sm'}),
            'email': forms.TextInput(attrs=default_widget | {'placeholder': 'name@example.com'}),
            'first_name': forms.TextInput(attrs=default_widget | {'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs=default_widget | {'placeholder': 'Фамилия'}),
            'is_subscribed_on_quotes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_subscribed_on_weather': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        label='Имя пользователя',
        disabled=True,
        widget=forms.TextInput(attrs=default_widget | {'placeholder': 'Имя пользователя'})
    )
    email = forms.EmailField(
        label='E-mail',
        disabled=True,
        widget=forms.EmailInput(attrs=default_widget)
    )
    date_birth = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'style':
                'margin-top:5px;'
                'background: #141214;'
                'border-color: #141214;'
                'color:white;',
        }))

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'username', 'email', 'first_name', 'last_name', 'date_birth',
                  'is_subscribed_on_quotes', 'is_subscribed_on_weather']

        widgets = {
            'avatar': forms.FileInput(attrs=default_widget | {'class': 'form-control-sm'}),
            'first_name': forms.TextInput(attrs=default_widget | {'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs=default_widget | {'placeholder': 'Фамилия'}),
            'is_subscribed_on_quotes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_subscribed_on_weather': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PasswordChangeUserForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль",
                                   min_length=6,
                                   max_length=20,
                                   widget=forms.PasswordInput(attrs=default_widget))
    new_password1 = forms.CharField(label="Новый пароль",
                                    min_length=6,
                                    max_length=20,
                                    widget=forms.PasswordInput(attrs=default_widget))
    new_password2 = forms.CharField(label="Повторите пароль",
                                    min_length=6,
                                    max_length=20,
                                    widget=forms.PasswordInput(attrs=default_widget))
