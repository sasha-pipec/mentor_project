from drf_yasg import openapi
from rest_framework import status

delete_photo_parameters = [
    openapi.Parameter('slug_id', openapi.IN_PATH,
                      description="Slug of photo",
                      type=openapi.TYPE_STRING,
                      ),
    openapi.Parameter('Authorization', openapi.IN_HEADER,
                      description="Needed give 'Token your_api_token'. Api_token can be generated in your personal "
                                  "account",
                      type=openapi.TYPE_STRING,
                      required=True),
]

delete_photo_response = {
    status.HTTP_201_CREATED: 'Successes',
    status.HTTP_409_CONFLICT: 'Incorrect value of slug_id',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
}
