from django import forms
from service_objects.services import Service
from photobatle import models


class DeleteLikeService(Service):
    """Service class for delete like"""

    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self):
        like = models.Likemodels.Like.objects.get(photo_id=self.cleaned_data['photo_id'],
                                                  user_id=self.cleaned_data['user_id'])
        like.delete()
        return (models.Photomodels.Photo.objects.get(pk=self.cleaned_data['photo_id'])).slug
