import re

from django.core.validators import RegexValidator
from rest_framework import serializers

phone_regex = re.compile('^(?:\+254)?(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$')


class ProfileSerializer(serializers.Serializer):
    """ Serializer that saves a user's profile information """

    first_name = serializers.CharField(
        max_length=30,
        min_length=1,
        required=True
    )
    last_name = serializers.CharField(
        max_length=30,
        min_length=1,
        required=True
    )
    phone = serializers.CharField(
        max_length=20,
        required=False,
        validators=[RegexValidator(phone_regex, message="Invalid Phone Number")],
        allow_blank=True
    )

    def validate_phone(self, value):
        # validate the format of the phone number
        return value

    def save(self, user):
        user.first_name = self.validated_data["first_name"]
        user.last_name = self.validated_data["last_name"]
        user.phone = self.validated_data.get("phone")
        user.save()
        return user
