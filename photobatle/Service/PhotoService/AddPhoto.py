from django import forms
from django.core.exceptions import ValidationError

from service_objects.services import Service
from photobatle import models
from transliterate import translit


class AddPhotoService(Service):
    """Service class for add photo"""

    photo_name = forms.CharField()
    photo_content = forms.CharField()
    photo = forms.Field()
    user_id = forms.IntegerField()

    def slug_russian_word(self, word):
        # Making a slug of Russian words
        russia = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        slug = ''
        for i in word:
            if i.lower() in russia:
                slug += translit(i, language_code='ru', reversed=True)
            else:
                if i == ' ':
                    slug += '-'
                else:
                    slug += i
        return slug

    def process(self):
        photo_name = self.cleaned_data['photo_name']
        photo_content = self.cleaned_data['photo_content']
        photo = self.cleaned_data['photo']
        user_id = self.cleaned_data['user_id']
        slug = self.slug_russian_word(self.cleaned_data['photo_name'])

        return models.Photomodels.Photo.objects.create(
            photo_name=photo_name,
            photo_content=photo_content,
            photo=photo,
            user_id=user_id,
            slug=slug
        )
