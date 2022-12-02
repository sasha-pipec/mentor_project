from drf_yasg import openapi
from rest_framework import status

PHOTO_RETRIEVE = {
    'manual_parameters': [
        openapi.Parameter('slug', openapi.IN_PATH,
                          description="The slug of photo",
                          type=openapi.TYPE_STRING,
                          )
    ],
    'responses': {
        status.HTTP_200_OK: 'Successes',
        status.HTTP_404_NOT_FOUND: 'Incorrect value of slug'
    }
}
