from rest_framework import serializers

from elections.models import Election
from seats.models import Seat


class AddSeatSerializer(serializers.Serializer):
    """
      Serializer to handle addition of elections
    """

    name = serializers.CharField(
        max_length=100,
        required=True
    )

    election_slug = serializers.SlugField(required=True)

    def validate(self, data):
        if not Election.objects.filter(slug=data["election_slug"]).exists():
            raise serializers.ValidationError("Election Slug is Not Valid")
        if Seat.objects.filter(name=data["name"].title(), election__slug=data["election_slug"]).exists():
            raise serializers.ValidationError("Seat Names must be Unique for every Election")
        return data

    def save(self, **kwargs):
        """
        Create an election using Validated Data
        """
        # get validated data
        name = self.validated_data["name"]
        election_slug = self.validated_data["election_slug"]

        # create and return an election instance
        return Seat.objects.create(
            name=name,
            election=Election.objects.get(slug=election_slug)
        )
