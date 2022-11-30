from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from actors.models import Actor
from movies.models import Movie
from actors.serializers import ActorSerializer
from mixins.viewsets import TakeHomeViewSet


class ActorViewSet(TakeHomeViewSet):
    """
    ViewSet for Actor model

    This ViewSet implements all the CRUD methods for the Actor model
    """

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CommonActorsViewSet(ViewSet):
    """
    ViewSet Model for actors that appear in all requested movies

    This ViewSet implements the list method to obtain the actors that appear
    in all requested movies by query params
    """

    def list(self, request):

        movies_qp = request.query_params.get('movies')

        # Check if movies query params exists in request

        if movies_qp is None:
            return Response(
                {
                    "detail": "movies query param is missing",
                    "status_code": status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        movies = set(movies_qp.split(","))

        # Check if all movies exists

        movies_in_db = {
            mov.title for mov in Movie.objects.filter(title__in=movies)
        }

        missing_movies = movies - movies_in_db

        if missing_movies:
            return Response(
                {
                    "detail":
                        f"The movies {','.join(missing_movies)} "
                        "doesn't exists",
                    "status_code": status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # If all is right reply response

        queryset = Actor.objects.filter(movies__in=movies).distinct()

        for movie in movies:
            queryset = queryset.filter(movies=movie)

        serializer = ActorSerializer(queryset, many=True)

        return Response(serializer.data)
