from rest_framework import status

USER_RETRIEVE = {
    'responses': {
        status.HTTP_200_OK: 'Successes',
        status.HTTP_401_UNAUTHORIZED: 'Incorrect value of Api_token'
    },
    'operation_description': 'You need to authorization'
}
