from drf_yasg import openapi
from rest_framework import status

patch_comment_parameters = [
    openapi.Parameter('id', openapi.IN_PATH,
                      description="The id of comment you want to edit",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('comment', openapi.IN_FORM,
                      description="The new comment for photo",
                      type=openapi.TYPE_STRING,
                      required=True),
]

patch_comment_response = {
    status.HTTP_201_CREATED: 'Successes',
    status.HTTP_404_NOT_FOUND: 'Incorrect value of id',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
}

patch_comment_description = 'You need to authorization'
