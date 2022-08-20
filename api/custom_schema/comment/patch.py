from drf_yasg import openapi
from rest_framework import status

patch_comment_parameters = [
    openapi.Parameter('Authorization', openapi.IN_HEADER,
                      description="Needed give 'Token your_api_token'. Api_token can be generated in your personal "
                                  "account",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('comment_pk', openapi.IN_PATH,
                      description="The pk of comment",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('comment', openapi.IN_FORM,
                      description="The new comment for photo",
                      type=openapi.TYPE_STRING,
                      required=True),
]

patch_comment_response = {
    status.HTTP_201_CREATED: 'Successes',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    status.HTTP_409_CONFLICT: 'Incorrect comment_pk values',
}
