from django import forms

from . import models

FRUIT_CHOICES = [
    ('like_count', 'Сортировка по лайкам'),
    ('comment_count', 'Сортировка по комментариям'),
    ('updated_at', 'Сортировка по дате'),
]

STATUS_CHOICES = (
    ('1', 'На удалении'),
    ('2', 'На модерации'),
    ('3', 'Одобренно'),
)


class SortForm(forms.Form):
    choice = forms.CharField(label='Сортировка', widget=forms.RadioSelect(choices=FRUIT_CHOICES))


class PersonalSortForm(forms.Form):
    choice = forms.CharField(label='Сортировка', widget=forms.RadioSelect(choices=STATUS_CHOICES))


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photomodels.Photo
        fields = ['photo', 'photo_name', 'photo_content']
        widgets = {
            'photo_name': forms.TextInput(attrs={'class': 'form-field'}),
            'photo_content': forms.Textarea(attrs={'class': 'form-field'}),
        }
