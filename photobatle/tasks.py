from photobatle.celery import app
from photobatle import models


@app.task
def delete_photo(slug):
    photo = models.Photomodels.Photo.objects.get(slug=slug)
    photo.delete()
    return 'Photo deleted'
