from drf_yasg import openapi
from rest_framework import status

get_home_photo_parameters = [
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
                      description="Number of page",
                      type=openapi.TYPE_NUMBER,
                      required=True),
]

get_home_photo_response = {
    status.HTTP_200_OK: 'Successes',
    status.HTTP_404_NOT_FOUND: 'Incorrect sort_value or direction or page',
}