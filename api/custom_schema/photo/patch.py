from drf_yasg import openapi
from rest_framework import status

patch_photo_parameters = [
    openapi.Parameter('slug', openapi.IN_PATH,
                      description="Slug of photo",
                      type=openapi.TYPE_STRING,
                      ),
    openapi.Parameter('photo', openapi.IN_FORM,
                      description="The new photo of post",
                      type=openapi.TYPE_FILE),
    openapi.Parameter('photo_name', openapi.IN_FORM,
                      description="The new photo_name of post",
                      type=openapi.TYPE_STRING),
    openapi.Parameter('photo_content', openapi.IN_FORM,
                      description="The new photo_content of post",
                      type=openapi.TYPE_STRING),
]

patch_photo_response = {
    status.HTTP_204_NO_CONTENT: 'Successes',
    status.HTTP_400_BAD_REQUEST: 'Incorrect value of slug or not required parameters',
    status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token',
}

patch_photo_operation_description = 'You need to authorization' \
                                    'If you want change your post, send one of all not required parameters'
