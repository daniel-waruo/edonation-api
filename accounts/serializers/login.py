from django.contrib.auth import authenticate
from django.contrib.auth.views import UserModel
from knox.models import AuthToken
from rest_framework import serializers

from accounts.utils import create_token, send_confirmation_email


class LoginSerializer(serializers.Serializer):
    """ DRF serializer that validates user credentials and returns user token if successful """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = UserModel.objects.get(email=email)
        print(user)
        # Did we get back an active user?
        if user.check_password(password):
            if not user.is_active:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg)

        # If required, is the email verified?
        if not user.email_confirmed:
            # send confirmation email
            send_confirmation_email(user)
            raise serializers.ValidationError('E-mail is not verified.\nCheck your email to verify')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        """get the user from the validated data and create the user's token"""
        user = self.validated_data['user']
        token = create_token(AuthToken, user, None)
        return token, user
