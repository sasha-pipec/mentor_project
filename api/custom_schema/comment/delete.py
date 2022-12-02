from drf_yasg import openapi
from rest_framework import status

COMMENT_DELETE = {
    'manual_parameters': [
        openapi.Parameter('id', openapi.IN_PATH,
                          description="The id of comment you want to delete",
                          type=openapi.TYPE_STRING,
                          required=True),
    ],
    'responses': {
        status.HTTP_204_NO_CONTENT: 'Successes',
        status.HTTP_404_NOT_FOUND: 'Incorrect value of id',
        status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
        status.HTTP_400_BAD_REQUEST: 'Comment has children or you dont author of this comment',
    },
    'operation_description': 'You need to authorization'
}
