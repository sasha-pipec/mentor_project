from django import forms
from . import models

FRUIT_CHOICES = [
    ('like_count', 'Сортировка по лайкам'),
    ('comment_count', 'Сортировка по комментариям'),
    ('date_published_on_site', 'Сортировка по дате'),
]


class SortForm(forms.Form):
    choice = forms.CharField(label='Сортировка', widget=forms.RadioSelect(choices=FRUIT_CHOICES))


class AddPhoto(forms.ModelForm):
    class Meta:
        model = models.Photomodels.Photo
        fields = ['photo', 'photo_name', 'photo_content']
