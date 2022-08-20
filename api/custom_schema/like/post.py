from drf_yasg import openapi
from rest_framework import status

post_like_parameters = [
    openapi.Parameter('Authorization', openapi.IN_HEADER,
                      description="Needed give 'Token your_api_token'. Api_token can be generated in your personal "
                                  "account",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('photo_id', openapi.IN_FORM,
                      description="The id of photo",
                      type=openapi.TYPE_INTEGER,
                      required=True),
]

post_like_response = {
    status.HTTP_201_CREATED: 'Successes',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    status.HTTP_409_CONFLICT: 'Incorrect photo_id values',
}
