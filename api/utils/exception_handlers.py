from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        response = Response(
            {
                "detail": str(exc),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )
    elif type(exc) == ParseError:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        response.data['detail'] = str(exc)
        response.data['status_code'] = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif response is not None:
        response.data['status_code'] = response.status_code

    return response
