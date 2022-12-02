from drf_yasg import openapi
from rest_framework import status

COMMENT_CREATE = {
    'manual_parameters': [
        openapi.Parameter('slug', openapi.IN_PATH,
                          description="The slug of photo",
                          type=openapi.TYPE_STRING,
                          ),
        openapi.Parameter('comment', openapi.IN_FORM,
                          description="The comment for photo",
                          type=openapi.TYPE_STRING,
                          required=True),
        openapi.Parameter('parent_comment_id', openapi.IN_FORM,
                          description="The id of parent comment",
                          type=openapi.TYPE_INTEGER),
    ],
    'responses': {
        status.HTTP_201_CREATED: 'Successes',
        status.HTTP_404_NOT_FOUND: 'Incorrect value of slug or parent_comment_id',
        status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    },
    'operation_description': 'You need to authorization'
}
