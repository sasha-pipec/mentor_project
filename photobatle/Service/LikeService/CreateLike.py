from django import forms
from service_objects.services import Service
from photobatle import models


class CreateLikeService(Service):
    """Service class for create like"""

    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self):
        photo_id = self.cleaned_data['photo_id']
        user_id = self.cleaned_data['user_id']

        models.Likemodels.Like.objects.create(photo_id=photo_id, user_id=user_id)
        return (models.Photomodels.Photo.objects.get(pk=photo_id)).slug

