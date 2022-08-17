from drf_yasg import openapi
from rest_framework import status

post_photo_parameters = [
    openapi.Parameter('Authorization', openapi.IN_HEADER,
                      description="Needed give 'Token your_api_token'. Api_token can be generated in your personal "
                                  "account",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('photo', openapi.IN_FORM,
                      description="The photo of post",
                      type=openapi.TYPE_FILE,
                      required=True),
    openapi.Parameter('photo_name', openapi.IN_FORM,
                      description="The new photo name for pos",
                      type=openapi.TYPE_STRING,
                      required=True),
    openapi.Parameter('photo_content', openapi.IN_FORM,
                      description="The new photo description for post",
                      type=openapi.TYPE_STRING,
                      required=True),
]

post_photo_response = {
    status.HTTP_201_CREATED: 'Successes',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
    status.HTTP_409_CONFLICT: 'Incorrect required parameters',
}
