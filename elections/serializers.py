from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from elections.models import Election


class ElectionSerializers(serializers.Serializer):
    """
    Serializer to handle addition of elections
    """
    name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(
            queryset=Election.objects.all(),
            message="Election Name must be Unique")
        ],
        required=True
    )

    start_date = serializers.DateTimeField(
        required=True
    )

    end_date = serializers.DateTimeField(
        required=True
    )

    active = serializers.BooleanField(required=False)

    def validate(self, data):
        """
        Check that start date is before end date
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End Date must occur after Start Date")
        return data

    def save(self, user):
        """
        Create an election using Validated Data
        """
        # get validated data
        name = self.validated_data["name"]
        start_date = self.validated_data["start_date"]
        end_date = self.validated_data["end_date"]

        # create and return an election instance
        return Election.objects.create(
            user=user,
            name=name,
            start_date=start_date,
            end_date=end_date
        )
