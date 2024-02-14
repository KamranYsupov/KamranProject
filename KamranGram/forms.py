from django import forms

from KamranGram.models import Room


class AddRoomForm(forms.ModelForm):
    password = forms.CharField(required=False, min_length=6, max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = Room
        fields = ['name', 'description', 'theme', 'password']
