from drf_yasg import openapi
from rest_framework import status

get_sort_personal_photo_parameters = [
    openapi.Parameter('sort_value', openapi.IN_QUERY,
                      description="You can choice one of the all parameters for sorting posts. form take: "
                                  "'DEL'-on delete,  'MOD'-on moderation, 'APR'-on approved , 'REJ'-on rejected",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('page', openapi.IN_QUERY,
                      description="Number of page",
                      type=openapi.TYPE_STRING,
                      required=True),
]

get_sort_personal_photo_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_400_BAD_REQUEST: 'Incorrect value of form',
}

get_sort_personal_photo_description = 'You need to authorization'
