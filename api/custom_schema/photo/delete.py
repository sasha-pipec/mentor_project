from drf_yasg import openapi
from rest_framework import status

delete_photo_parameters = [
    openapi.Parameter('slug', openapi.IN_PATH,
                      description="The slug of photo",
                      type=openapi.TYPE_STRING,
                      ),
]

delete_photo_response = {
    status.HTTP_204_NO_CONTENT: 'Successes',
    status.HTTP_404_NOT_FOUND: 'Incorrect value of slug',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
}

delete_photo_description = 'You need to authorization'
