from drf_yasg import openapi
from rest_framework import status

patch_comment_parameters = [
    openapi.Parameter('comment_id', openapi.IN_PATH,
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
    status.HTTP_400_BAD_REQUEST: 'Incorrect comment_id values',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
}

patch_comment_description = 'You need to authorization'
