from rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer
from rest_framework import serializers


class RegisterSerializer(BaseRegisterSerializer):
    """ DRF Serializer responsible for creating a new user in the data base

     This class also sends a confirmation email if the user is successfully saved

    """

    first_name = serializers.CharField(
        max_length=255,
        min_length=1,
        required=True
    )
    last_name = serializers.CharField(
        max_length=255,
        min_length=1,
        required=True
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        })
        return data
