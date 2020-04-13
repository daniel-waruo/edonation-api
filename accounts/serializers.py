from allauth.account import app_settings
from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import authenticate
from rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer
from rest_auth.serializers import (
    PasswordResetSerializer as ResetPasswordSerializer,
    UserDetailsSerializer,
    LoginSerializer as BaseLoginSerializer,
)
from rest_framework import serializers

from accounts.models import User


class KnoxSerializer(serializers.Serializer):
    """
      KnoxSerializer
      Serializer for Knox library authentication authentication.
    """
    token = serializers.CharField()
    user = UserDetailsSerializer()


# serializer for logging in a user
class LoginSerializer(BaseLoginSerializer):
    """
    Login
    Serializer for handling login in our application
    it inherits from Login Serializer and is tweaked for
    login using Knox library
    """

    def validate(self, attrs):
        # get data
        email = attrs.get('email')
        password = attrs.get('password')

        # check whether the user credentials are valid
        user = self._validate_username_email(None, email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg)

        if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
            email_address, isCreated = user.emailaddress_set.get_or_create(email=user.email)
            if not email_address.verified:
                send_email_confirmation(self.context["request"], user)
                raise serializers.ValidationError('E-mail is not verified.Check your email')
        attrs['user'] = user
        return attrs


class RegisterSerializer(BaseRegisterSerializer):
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


# serializer for changing a password
class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'password'
        ]
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        User.objects.get(
            username=validated_data["username"]
        ).set_password(validated_data["new_password"])

    def validate(self, data):
        user = authenticate(
            **{
                "username": data["username"],
                "password": data["current_password"],
            }
        )
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class PasswordResetSerializer(ResetPasswordSerializer):
    password_reset_form_class = ResetPasswordForm
