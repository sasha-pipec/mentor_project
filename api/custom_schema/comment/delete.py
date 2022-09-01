from drf_yasg import openapi
from rest_framework import status

delete_comment_parameters = [
    openapi.Parameter('Authorization', openapi.IN_HEADER,
                      description="Needed give 'Token your_api_token'. Api_token can be generated in your personal "
                                  "account",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('comment_id', openapi.IN_PATH,
                      description="The pk of comment",
                      type=openapi.TYPE_STRING,
                      required=True),
]

delete_comment_response = {
    status.HTTP_204_NO_CONTENT: 'Successes',
    status.HTTP_400_BAD_REQUEST: 'Comment have children',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    status.HTTP_409_CONFLICT: 'Incorrect comment_id values',
}