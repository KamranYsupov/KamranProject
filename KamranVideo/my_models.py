from django.core.files.images import get_image_dimensions
from django.db.models import ImageField, FileField
from django import forms
from django.template.defaultfilters import filesizeformat

from django.conf import settings


class LimitedImageField(ImageField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = settings.MAX_IMAGE_MEMORY_SIZE
        super(LimitedImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(LimitedImageField, self).clean(*args, **kwargs)
        try:
            img_file = data.file
            if img_file.size > self.max_upload_size:
                error_message = 'Размер файла не должен превышать {}'.format(filesizeformat(self.max_upload_size))
                raise forms.ValidationError(error_message)

            w, h = get_image_dimensions(img_file)
            if (w / h) != (16 / 9):
                error_message = 'Изображения должно быть в формате 16x9'
                raise forms.ValidationError(error_message)
        except AttributeError:
            pass
        return data


class VideoField(FileField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop('max_video_size', None)
        if not self.max_upload_size:
            self.max_upload_size = settings.MAX_VIDEO_MEMORY_SIZE
        super(VideoField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(VideoField, self).clean(*args, **kwargs)
        try:
            video_file = data.file
            if video_file.size > self.max_upload_size:
                error_message = 'Размер файла не должен превышать {}'.format(filesizeformat(self.max_upload_size))
                raise forms.ValidationError(error_message)
        except AttributeError:
            pass
        return data

