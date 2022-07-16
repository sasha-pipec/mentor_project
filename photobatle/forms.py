from django import forms
from django.core.exceptions import ValidationError

from . import models

FRUIT_CHOICES = [
    ('like_count', 'Сортировка по лайкам'),
    ('comment_count', 'Сортировка по комментариям'),
    ('updated_at', 'Сортировка по дате'),
]


class SortForm(forms.Form):
    choice = forms.CharField(label='Сортировка', widget=forms.RadioSelect(choices=FRUIT_CHOICES))


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photomodels.Photo
        fields = ['photo', 'photo_name', 'photo_content']
        widgets = {
            'photo_name': forms.TextInput(attrs={'class': 'form-field'}),
            'photo_content': forms.Textarea(attrs={'class': 'form-field'}),
        }

    def clean_photo(self):
        # Checking the type of the downloaded file
        if (self.cleaned_data['photo'].content_type).split('/')[1] != 'jpeg':
            raise ValidationError('Тип загружаемого файла не JPEG, повторите попытку')
        return self.cleaned_data['photo']
