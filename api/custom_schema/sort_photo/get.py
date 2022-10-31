from drf_yasg import openapi
from rest_framework import status

get_sort_photo_parameters = [
    openapi.Parameter('sort_value', openapi.IN_QUERY,
                      description="You can choice one of the all parameters for sorting posts. form take: "
                                  "'like_count',  'comment_count', 'updated_at'",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('search_value', openapi.IN_QUERY,
                      description="You can find a concrete post, enter the keywords for this",
                      type=openapi.TYPE_STRING),
    openapi.Parameter('page', openapi.IN_QUERY,
                      description="Number of page",
                      type=openapi.TYPE_STRING,
                      required=True),
]

get_sort_photo_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_400_BAD_REQUEST: 'Incorrect value of form',

}

get_sort_photo_operation_description = 'If you want send sort request, enter one of all sorting parameters, and not ' \
                                       'required parameters: search keyword. For search request send only keyword ' \
                                       'parameter '
