from drf_yasg import openapi
from rest_framework import status

PHOTO_PATCH = {
    'manual_parameters': [
        openapi.Parameter('slug', openapi.IN_PATH,
                          description="The slug of photo",
                          type=openapi.TYPE_STRING,
                          ),
        openapi.Parameter('photo', openapi.IN_FORM,
                          description="The new photo of post",
                          type=openapi.TYPE_FILE),
        openapi.Parameter('name', openapi.IN_FORM,
                          description="The new name of post",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('content', openapi.IN_FORM,
                          description="The new content of post",
                          type=openapi.TYPE_STRING),
    ],
    'responses': {
        status.HTTP_204_NO_CONTENT: 'Successes',
        status.HTTP_404_NOT_FOUND: 'Incorrect value of slug',
        status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    },
    'operation_description': 'You need to authorization' \
                             'If you want change your post, send one of all not required parameters'
}
