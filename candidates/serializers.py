from pyuploadcare import InvalidRequestError, File
from rest_framework import serializers

from candidates.models import Candidate
from seats.models import Seat


def image_validator(value):
    try:
        return File(value).cdn_url
    except InvalidRequestError as exc:
        raise serializers.ValidationError(
            'Invalid value for Image field {exc}'.format(exc=exc)
        )


class AddCandidateSerializer(serializers.Serializer):
    """
      Serializer to handle addition of elections
    """

    first_name = serializers.CharField(
        max_length=100,
        required=True
    )
    last_name = serializers.CharField(
        max_length=100,
        required=True
    )

    image = serializers.URLField(validators=[image_validator])

    def validate_image(self, value):
        file = File(value)
        file.info()
        return value

    email = serializers.EmailField()

    seat_id = serializers.CharField(required=True)

    def validate_email(self, value):
        seat_id = self.initial_data["seat_id"]
        if Candidate.objects.filter(email=value.lower(), seat__id=seat_id).exists():
            raise serializers.ValidationError("Emails must be Unique for every Candidate")
        return value

    def validate_seat_id(self, value):
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("Seat Id Must be a Valid Integer Not Valid")
        return value

    def validate(self, data):
        # check if seat ID is valid
        if not Seat.objects.filter(id=data["seat_id"], election__user=self.context.user).exists():
            raise serializers.ValidationError("Seat ID {} is Not Valid".format(data["seat_id"]))
        return data

    def get_validated_data(self):
        # save image before saving to db
        image = self.validated_data["image"]
        # store the file
        File(image).store()
        return {
            "first_name": self.validated_data["first_name"],
            "last_name": self.validated_data["last_name"],
            "email": self.validated_data["email"],
            "image": image,
            "seat": Seat.objects.get(id=self.validated_data["seat_id"])
        }

    def save(self, **kwargs):
        """
          Store Candidate in DB using Validated Data
        """
        # get validated data
        data = self.get_validated_data()
        # create and return an election instance
        return Candidate.objects.create(**data)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
