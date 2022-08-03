from django import forms
from service_objects.services import Service
from photobatle import models


class CreateLikeService(Service):
    """Service class for create like"""

    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self):
        models.Likemodels.Like.objects.create(photo_id=self.cleaned_data['photo_id'],
                                              user_id=self.cleaned_data['user_id'])
        return (models.Photomodels.Photo.objects.get(pk=self.cleaned_data['photo_id'])).slug
