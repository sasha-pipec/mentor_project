from drf_yasg import openapi
from rest_framework import status

GENERAL_PHOTO_LIST = {
    'manual_parameters': [
        openapi.Parameter('sort_value', openapi.IN_QUERY,
                          description="You can choice one of the all parameters for sorting posts. form take: "
                                      "'like_count',  'comment_count', 'updated_at'",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('search_value', openapi.IN_QUERY,
                          description="You can find a concrete post, enter the keywords for this",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('direction', openapi.IN_QUERY,
                          description="You can choice asc-ascending or desc-descending direction",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY,
                          description="You can specify the page number,"
                                      " the values taken from the first page will be returned by default",
                          type=openapi.TYPE_NUMBER,
                          required=False),
        openapi.Parameter('per_page', openapi.IN_QUERY,
                          description="you can choose the number of photos per page",
                          type=openapi.TYPE_NUMBER,
                          required=False),
    ],
    'responses': {
        status.HTTP_200_OK: 'Successes',
        status.HTTP_404_NOT_FOUND: 'Incorrect value of sort, direction or page',
    },
}
