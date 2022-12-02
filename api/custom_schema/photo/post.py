from drf_yasg import openapi
from rest_framework import status

PHOTO_CREATE = {
    'manual_parameters': [
        openapi.Parameter('photo', openapi.IN_FORM,
                          description="The photo of post",
                          type=openapi.TYPE_FILE,
                          required=True),
        openapi.Parameter('name', openapi.IN_FORM,
                          description="The name for post",
                          type=openapi.TYPE_STRING,
                          required=True),
        openapi.Parameter('content', openapi.IN_FORM,
                          description="The content for post",
                          type=openapi.TYPE_STRING,
                          required=True),
    ],
    'responses': {
        status.HTTP_201_CREATED: 'Successes',
        status.HTTP_400_BAD_REQUEST: 'Incorrect required parameters or some conflict',
        status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    },
    'operation_description': 'You need to authorization'
}
