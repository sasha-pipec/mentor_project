from drf_yasg import openapi
from rest_framework import status

delete_like_parameters = [
    openapi.Parameter('photo_id', openapi.IN_PATH,
                      description="The id of photo",
                      type=openapi.TYPE_INTEGER,
                      required=True),
]

delete_like_response = {
    status.HTTP_204_NO_CONTENT: 'Successes',
    status.HTTP_400_BAD_REQUEST: 'Incorrect photo_id values',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
}

delete_like_description = 'You need to authorization'