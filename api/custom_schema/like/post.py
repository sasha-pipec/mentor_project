from drf_yasg import openapi
from rest_framework import status

post_like_parameters = [
    openapi.Parameter('slug', openapi.IN_PATH,
                      description="The slug of photo",
                      type=openapi.TYPE_STRING,
                      required=True),
]

post_like_response = {
    status.HTTP_201_CREATED: 'Successes',
    status.HTTP_404_NOT_FOUND: 'Incorrect  value of slug',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
}

post_like_description = 'You need to authorization'
