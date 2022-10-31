from drf_yasg import openapi
from rest_framework import status

delete_comment_parameters = [
    openapi.Parameter('comment_id', openapi.IN_PATH,
                      description="The pk of comment",
                      type=openapi.TYPE_STRING,
                      required=True),
]

delete_comment_response = {
    status.HTTP_204_NO_CONTENT: 'Successes',
    status.HTTP_400_BAD_REQUEST: 'Incorrect comment_id values',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    status.HTTP_409_CONFLICT: 'Comment have children',
}

delete_comment_description = 'You need to authorization'
