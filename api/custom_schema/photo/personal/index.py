from drf_yasg import openapi
from rest_framework import status

PERSONAL_PHOTO_LIST = {
    'manual_parameters': [
        openapi.Parameter('sort_value', openapi.IN_QUERY,
                          description="You can choice one of the all parameters for sorting posts. form take: "
                                      "'DELETION'-on delete,  'MODERATION'-on moderation,"
                                      "'APPROVED'-on approved , 'REJECTED'-on rejected",
                          type=openapi.TYPE_STRING, ),
        openapi.Parameter('page', openapi.IN_QUERY,
                          description="You can specify the page number,"
                                      "the values taken from the first page will be returned by default",
                          type=openapi.TYPE_NUMBER, ),
        openapi.Parameter('per_page', openapi.IN_QUERY,
                          description="you can choose the number of photos per page",
                          type=openapi.TYPE_NUMBER,
                          required=False),
    ],
    'responses': {
        status.HTTP_200_OK: 'Successes',
        status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
        status.HTTP_404_NOT_FOUND: 'Incorrect value of sort or page'
    },
    'operation_description': 'You need to authorization'
}
