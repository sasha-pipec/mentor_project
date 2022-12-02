from drf_yasg import openapi
from rest_framework import status

LIKE_TOGGLE = {
    'manual_parameters': [
        openapi.Parameter('slug', openapi.IN_PATH,
                          description="The slug of photo",
                          type=openapi.TYPE_STRING,
                          required=True),
    ],
    'responses': {
        status.HTTP_201_CREATED: 'Successes',
        status.HTTP_404_NOT_FOUND: 'Incorrect  value of slug',
        status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    },
    'operation_description': 'You need to authorization'
}
