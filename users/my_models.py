from django import forms
from django.core.files.images import get_image_dimensions
from django.db.models import ImageField


class AvatarImageField(ImageField):
    def __init__(self, *args, **kwargs):
        super(AvatarImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(AvatarImageField, self).clean(*args, **kwargs)
        try:
            avatar_file = data.file
            w, h = get_image_dimensions(avatar_file)

            if int((w / h) * 100) in list(range(90, 110)):
                pass
            else:
                error_message = 'Некорректный формат изображения'
                raise forms.ValidationError(error_message)

        except AttributeError:
            pass

        return data
