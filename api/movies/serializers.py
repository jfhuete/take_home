from rest_framework.serializers import ModelSerializer
from movies.models import Movie


class MovieSerializer(ModelSerializer):
    """
    Serializer for Movie Model

    This serializer define the necessary fields in Movie endpoints for
    requests and reply
    """

    class Meta:
        model = Movie
        fields = '__all__'
