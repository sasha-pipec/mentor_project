from drf_yasg import openapi
from rest_framework import status

get_personal_photo_parameters = [

]
get_personal_photo_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token'
}

get_personal_photo_description = 'You need to authorization'