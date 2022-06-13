from django import forms

FRUIT_CHOICES = [
    ('like_count', 'Сортировка по лайкам'),
    ('comment_count', 'Сортировка по комментариям'),
    ('date_published_on_site', 'Сортировка по дате'),
]


class SortForm(forms.Form):
    choice = forms.CharField(label='Сортировка', widget=forms.RadioSelect(choices=FRUIT_CHOICES))

