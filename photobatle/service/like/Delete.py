from django import forms
from service_objects.services import Service
from photobatle import models


class DeleteLikeService(Service):
    """Service class for delete like"""

    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    @property
    def validate_photo_id(self):
        try:
            models.Photomodels.Photo.objects.get(pk=self.cleaned_data['photo_id'])
        except Exception:
            raise Exception(f"Incorrect photo_id value")
        return True

    @property
    def get_like(self):
        try:
            models.Likemodels.Like.objects.get(photo_id=self.cleaned_data['photo_id'],
                                               user_id=self.cleaned_data['user_id'])
            return True
        except Exception:
            raise Exception(f"Photo dont have like from this user")

    def process(self):
        if self.validate_photo_id:
            if self.get_like:
                like = models.Likemodels.Like.objects.get(photo_id=self.cleaned_data['photo_id'],
                                                          user_id=self.cleaned_data['user_id'])
                like.delete()
                return (models.Photomodels.Photo.objects.get(pk=self.cleaned_data['photo_id'])).slug
