from django import forms


def room_name_validator(value):
    if ',' in value:
        raise forms.ValidationError('Название комнаты не должно включать в себя запятые')
