from drf_yasg import openapi
from rest_framework import status

post_comment_parameters = [
    openapi.Parameter('Authorization', openapi.IN_HEADER,
                      description="Needed give 'Token your_api_token'. Api_token can be generated in your personal "
                                  "account",
                      type=openapi.TYPE_STRING,
                      required=True),
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
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    status.HTTP_409_CONFLICT: 'Incorrect slug or parent_comment_id values',
}
