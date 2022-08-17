from drf_yasg import openapi
from rest_framework import status

get_user_parameters = [
    openapi.Parameter('Authorization', openapi.IN_HEADER,
                      description="Needed give 'Token your_api_token'. Api_token can be generated in your personal "
                                  "account",
                      type=openapi.IN_HEADER,
                      required=True)
]
get_user_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token'
}
