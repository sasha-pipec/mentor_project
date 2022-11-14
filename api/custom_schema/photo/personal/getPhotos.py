from drf_yasg import openapi
from rest_framework import status

get_personal_photo_parameters = [
    openapi.Parameter('sort_value', openapi.IN_QUERY,
                      description="You can choice one of the all parameters for sorting posts. form take: "
                                  "'DEL'-on delete,  'MOD'-on moderation, 'APR'-on approved , 'REJ'-on rejected",
                      type=openapi.TYPE_STRING,),
    openapi.Parameter('page', openapi.IN_QUERY,
                      description="Number of page",
                      type=openapi.TYPE_NUMBER,
                      required=True),
]
get_personal_photo_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    status.HTTP_404_NOT_FOUND: 'Incorrect sort value or page'
}

get_personal_photo_description = 'You need to authorization'
