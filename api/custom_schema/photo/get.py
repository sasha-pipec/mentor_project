from drf_yasg import openapi
from rest_framework import status

get_photo_parameters = [
    openapi.Parameter('slug', openapi.IN_PATH,
                      description="The slug of photo",
                      type=openapi.TYPE_STRING,
                      )]

get_photo_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_409_CONFLICT: 'Incorrect value of slug'
}

