from drf_yasg import openapi
from rest_framework import status

get_user_parameters = [

]
get_user_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token'
}

get_user_description = 'You need to authorization'
