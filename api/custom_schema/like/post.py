from drf_yasg import openapi
from rest_framework import status

post_like_parameters = [
    openapi.Parameter('photo_id', openapi.IN_FORM,
                      description="The id of photo",
                      type=openapi.TYPE_INTEGER,
                      required=True),
]

post_like_response = {
    status.HTTP_201_CREATED: 'Successes',
    status.HTTP_400_BAD_REQUEST: 'Incorrect photo_id values',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
}

post_like_description = 'You need to authorization'
