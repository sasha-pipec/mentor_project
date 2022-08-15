from django import forms
from service_objects.services import Service
from photobatle import models


class CreateLikeService(Service):
    """Service class for create like"""

    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    @property
    def validate_photo_id(self):
        try:
            photo = models.Photomodels.Photo.objects.get(pk=self.cleaned_data['photo_id'])
            if photo.user.id == self.cleaned_data['user_id']:
                raise Exception(f"You cant create like, because it is your photo")
        except Exception:
            raise Exception(f"Incorrect photo_id value")
        return True

    @property
    def get_like(self):
        if not models.Likemodels.Like.objects.filter(photo_id=self.cleaned_data['photo_id'],
                                                     user_id=self.cleaned_data['user_id']):
            return True
        raise Exception(f"Photo can have one like from one user")

    def process(self):
        if self.validate_photo_id:
            if self.get_like:
                models.Likemodels.Like.objects.create(photo_id=self.cleaned_data['photo_id'],
                                                      user_id=self.cleaned_data['user_id'])
                return (models.Photomodels.Photo.objects.get(pk=self.cleaned_data['photo_id'])).slug
