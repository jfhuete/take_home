from rest_framework import serializers
from actors.models import Actor


class ActorSerializer(serializers.ModelSerializer):
    """
    Serializer for Actor Model

    This serializer define the necessary fields in Actor endpoints for
    requests and reply
    """

    gender = serializers.ChoiceField(
        choices=list(map(lambda g: (g[1], g[1]), Actor.GENDERS)),
        source='get_gender_display'
    )

    class Meta:
        model = Actor
        fields = '__all__'

    def map_display_gender_to_chart_gender(self, validated_data):
        """
        This method transform display gender to chart gender

        Note:

        validated_data is a dict, and dict is passed to fuction by reference,
        all changes in validated_data will be reflected in the context that
        has call this function

        :param validated_data: Request data validated
        :type validated_data: dict
        """

        gender = validated_data["get_gender_display"]
        selected_gender = next(g for g in Actor.GENDERS if g[1] == gender)
        validated_data["gender"] = selected_gender[0]

        del validated_data["get_gender_display"]

    def create(self, validated_data):
        """
        Override create method to change male | female by m | f

        :param validated_data: Request data validated
        :type validated_data: dict
        :return: Actor instance created
        :rtype: class: `actors.models.Actor`
        """

        self.map_display_gender_to_chart_gender(validated_data)
        actor = Actor(**validated_data)
        actor.save()

        return actor

    def update(self, instance, validated_data):
        """
        Override update method to change male | female by m | f

        :param instance: Actor instance of the update request
        :type instance: class: `actors.models.Actor`
        :param validated_data: Request data validated
        :type validated_data: dict
        :return: Actor instance updated
        :rtype: class: `actors.models.Actor`
        """

        self.map_display_gender_to_chart_gender(validated_data)

        return super().update(instance, validated_data)
