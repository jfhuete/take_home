from rest_framework.viewsets import ModelViewSet
from rest_framework import status


class TakeHomeViewSet(ModelViewSet):
    """
    ViewSet to customized response codes according requirements specification

    Some REST methods specified in the requirements return different status
    codes than those returned by rest framework by default. This class
    cusotmize this status codes
    """

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)

        # The specification for the correct status code for creation is 200 OK
        # instead of 201 Created, used by rest framework

        response.status_code = response.status_code \
            if response.status_code != status.HTTP_201_CREATED \
            else status.HTTP_200_OK

        return response
