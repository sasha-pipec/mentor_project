from drf_yasg import openapi
from rest_framework import status

post_comment_parameters = [
    openapi.Parameter('photo_slug', openapi.IN_FORM,
                      description="The slug of photo",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('comment', openapi.IN_FORM,
                      description="The comment for photo",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('parent_comment_id', openapi.IN_FORM,
                      description="The id of parent comment",
                      type=openapi.TYPE_INTEGER),
]

post_comment_response = {
    status.HTTP_201_CREATED: 'Successes',
    status.HTTP_400_BAD_REQUEST: 'Incorrect slug or parent_comment_id values',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
}

post_comment_description = 'You need to authorization'
