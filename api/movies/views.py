from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from actors.models import Actor
from movies.models import Movie
from movies.serializers import MovieSerializer
from mixins.viewsets import TakeHomeViewSet


class MovieViewSet(TakeHomeViewSet):
    """
    ViewSet for Movie model

    This ViewSet implements all the CRUD methods for the Movie model
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class PerformancesViewSet(ViewSet):
    """
    ViewSet Model for movies in which actors act

    This ViewSet implements the list method to obtain the movies in which the
    actors passed by queryparam act.
    """

    def list(self, request):

        actors_qp = request.query_params.get('actors')

        # Check if actors query params exists in request

        if actors_qp is None:
            return Response(
                {
                    "detail": "actors query param is missing",
                    "status_code": status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        actors = set(actors_qp.split(","))

        # Check if all actors exists

        actors_in_db = {
            act.name for act in Actor.objects.filter(name__in=actors)
        }

        missing_actors = actors - actors_in_db

        if missing_actors:
            return Response(
                {
                    "detail":
                        f"The actors {','.join(missing_actors)} "
                        "doesn't exists",
                    "status_code": status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # If all is right reply response

        queryset = Movie.objects.filter(cast__in=actors).distinct()

        for actor in actors:
            queryset = queryset.filter(cast=actor)

        serializer = MovieSerializer(queryset, many=True)

        return Response(serializer.data)
