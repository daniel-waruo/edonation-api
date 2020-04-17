from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from elections.models import Election


def id_validator(value):
    try:
        int(value)
    except ValueError:
        raise serializers.ValidationError("Id Must be a Valid Integer Not Valid")
    return value


class ElectionSerializer(serializers.Serializer):
    """
      Serializer to handle addition of elections
    """
    id = serializers.CharField(required=False, validators=[id_validator])

    name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(
            queryset=Election.objects.all(),
            message="Election Name must be Unique")
        ]
    )

    start_date = serializers.DateTimeField()

    end_date = serializers.DateTimeField()

    active = serializers.BooleanField(required=False)

    def validate(self, data):
        """
          Check that start date is before end date
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End Date must occur after Start Date")
        return data

    def create(self, validated_data):
        return Election.objects.create(
            user=self.context.user,
            **validated_data
        )

    def update(self, instance, validated_data):
        # if instance update the data instance
        instance.name = self.validated_data["name"]
        instance.start_date = self.validated_data["start_date"]
        instance.end_date = self.validated_data["end_date"]
        instance.save()
        return instance

    def save(self):
        """
          Create an election using Validated Data
        """
        # there is an update data in the database
        if self.instance:
            return self.update(self.instance, self.validated_data)
        # else create a new election
        return self.create(self.validated_data)


class DeleteElectionSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, value):
        user = self.context.user
        if not user.check_password(value):
            raise serializers.ValidationError("wrong password")
        return value

    def save(self):
        password = self.validated_data["password"]
        self.instance.delete()
