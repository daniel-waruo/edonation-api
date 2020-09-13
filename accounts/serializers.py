from allauth.account import app_settings
from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import authenticate
from rest_auth.app_settings import create_token
from rest_auth.models import TokenModel
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
    """ LoginSerializer
        Serializer for handling login in our application
        it inherits from Login Serializer and is tweaked for
        login using Knox library.
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

    def save(self, **kwargs):
        user = self.validated_data['user']
        token = create_token(TokenModel, user, None)
        return token, user


class CreateAdminUserSerializer(serializers.Serializer):
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
    phone = serializers.CharField(max_length=20)

    def validate_phone(self, value):
        if User.objects.filter(phone=value):
            raise serializers.ValidationError("Phone number must be unique")
        return value

    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(phone=value):
            raise serializers.ValidationError("Email must be unique")
        return value

    def save(self, **kwargs):
        user = User.objects.create_admin_user(
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            phone=self.validated_data["phone"],
            email=self.validated_data["email"],
            creator=self.context["request"].user
        )
        # send email to user to set their own password
        send_email_confirmation()
        return user


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
        fields = ['password']
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
        if not user or not user.is_active:
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        return data


class PasswordResetSerializer(ResetPasswordSerializer):
    password_reset_form_class = ResetPasswordForm


class ProfileSerializer(serializers.Serializer):
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
    phone = serializers.CharField(max_length=20, required=True)

    def validate_phone(self, value):
        # validate the format of the phone number
        return value
