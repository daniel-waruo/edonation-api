from allauth.account import app_settings
from allauth.account.utils import send_email_confirmation
from rest_auth.app_settings import create_token
from rest_auth.models import TokenModel
from rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from rest_framework import serializers


class LoginSerializer(BaseLoginSerializer):
    """ DRF serializer that validates user credentials and returns user token if successful """

    def validate(self, attrs):
        """ method that check the user login credentials and raises and error if not valid"""
        # get data provided to the serializer
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
        # check if the email of the user is verified if not raise a validation error
        # after sending the email
        if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
            email_address, isCreated = user.emailaddress_set.get_or_create(email=user.email)
            if not email_address.verified:
                send_email_confirmation(self.context["request"], user)
                raise serializers.ValidationError('E-mail is not verified.Check your email')
        # add user instance to the validated attributes for later saving if valid
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        """get the user from the validated data and create the user's token"""
        user = self.validated_data['user']
        token = create_token(TokenModel, user, None)
        return token, user
