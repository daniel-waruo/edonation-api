from rest_framework import serializers

from accounts.models import User
from accounts.utils import send_confirmation_email


class RegisterSerializer(serializers.Serializer):
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
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "A user is already registered with this e-mail address."
            )
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        # create db instance for user
        user: User = User.objects.create(**self.cleaned_data)
        # send email confirm email
        send_confirmation_email(user)
        return user

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
