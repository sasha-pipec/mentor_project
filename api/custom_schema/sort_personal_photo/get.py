from drf_yasg import openapi
from rest_framework import status

get_sort_personal_photo_parameters = [
    openapi.Parameter('form', openapi.IN_QUERY,
                      description="You can choice one of the all parameters for sorting posts. form take: "
                                  "'DEL',  'MOD', 'APR' , 'REJ'",
                      type=openapi.TYPE_STRING),
    openapi.Parameter('Authorization', openapi.IN_HEADER,
                      description="Needed give 'Token your_api_token'. Api_token can be generated in your personal "
                                  "account",
                      type=openapi.TYPE_STRING,
                      required=True)
]

get_sort_personal_photo_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_409_CONFLICT: 'Incorrect value of form',

}

