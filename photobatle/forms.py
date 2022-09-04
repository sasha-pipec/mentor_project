from django import forms
from photobatle.models import *

FRUIT_CHOICES = [
    ('like_count', 'Сортировка по лайкам'),
    ('comment_count', 'Сортировка по комментариям'),
    ('updated_at', 'Сортировка по дате'),
]

ON_DELETION = 'DEL'
ON_MODERATION = 'MOD'
APPROVED = 'APR'
REJECTED = 'REJ'

STATUS_CHOICES = (
    (ON_DELETION, 'На удалении'),
    (ON_MODERATION, 'На модерации'),
    (APPROVED, 'Одобренно'),
    (REJECTED, 'Отклоненно'),
)


class SortForm(forms.Form):
    choice = forms.CharField(label='Сортировка', widget=forms.RadioSelect(choices=FRUIT_CHOICES))


class PersonalSortForm(forms.Form):
    choice = forms.CharField(label='Сортировка', widget=forms.RadioSelect(choices=STATUS_CHOICES))


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photo', 'photo_name', 'photo_content']
        widgets = {
            'photo_name': forms.TextInput(attrs={'class': 'form-field'}),
            'photo_content': forms.Textarea(attrs={'class': 'form-field'}),
        }
