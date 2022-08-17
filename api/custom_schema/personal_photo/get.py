from drf_yasg import openapi
from rest_framework import status

get_personal_photo_parameters = [
    openapi.Parameter('Authorization', openapi.IN_HEADER,
                      description="Needed give 'Token your_api_token'. Api_token can be generated in your personal "
                                  "account",
                      type=openapi.TYPE_STRING,
                      required=True)
]
get_personal_photo_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token'
}