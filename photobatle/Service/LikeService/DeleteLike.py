from django import forms
from service_objects.services import Service
from photobatle import models


class DeleteLikeService(Service):
    """Service class for add photo"""

    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self):
        photo_id = self.cleaned_data['photo_id']
        user_id = self.cleaned_data['user_id']

        like = models.Likemodels.Like.objects.get(photo_id=photo_id, user_id=user_id)
        return like.delete()

