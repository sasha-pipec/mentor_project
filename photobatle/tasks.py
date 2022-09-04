from photobatle.celery import app
from photobatle.models import *


@app.task
def delete_photo(slug):
    photo = Photo.objects.get(slug=slug)
    photo.delete()
    return 'Photo deleted'
