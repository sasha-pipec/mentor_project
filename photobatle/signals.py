from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile
from allauth.account.signals import user_logged_in
from . import models


def social_signal(request, user, **kwargs):
    """Signal after successes authorization from vl / control photo"""
    list_data = kwargs['sociallogin'].account.extra_data
    name = urlparse(list_data['photo']).path.split('/')[-1]
    response = requests.get(list_data['photo'])
    path_photo = str(models.User.objects.get(username=list_data['screen_name']).photo).split('/')[-1]
    if path_photo != name:
        models.User.objects.get(username=list_data['screen_name']).photo.save(name, ContentFile(response.content),
                                                                              save=True)


user_logged_in.connect(social_signal)
