from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import complete_signup
from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.http import JsonResponse
from graphene_django.views import GraphQLView
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView, PasswordResetView as BasePasswordResetView
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import (AllowAny)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .serializers import PasswordResetSerializer, KnoxSerializer, LoginSerializer, RegisterSerializer
from .utils import create_knox_token


class KnoxLoginView(LoginView):
    serializer_class = LoginSerializer

    def get_response(self):
        # get ther serializer for response
        serializer_class = self.get_response_serializer()
        # set data to be sent to client
        data = {
            'user': self.user,
            'token': self.token
        }
        # create an instance of the serializer
        serializer = serializer_class(instance=data, context={'request': self.request})
        # return the response object
        return Response(serializer.data, status=200)


class KnoxRegisterView(RegisterView):
    serializer_class = RegisterSerializer

    def get_response_data(self, user):
        # check if email verification in mandatory then return a response saying the
        # verification email has been sent for the user to comfirm their email
        if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": "Verification e-mail sent."}
        # return serializer response
        return KnoxSerializer({'user': user, 'token': self.token}).data

    def perform_create(self, serializer):
        # create a user using the save method of the serializer
        user = serializer.save(self.request)
        # get token from create knox token
        self.token = create_knox_token(self.token_model, user, None)
        # complete the signup process
        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None)
        # return an instance of the user that has been created
        return user


class PasswordResetView(BasePasswordResetView):
    # set custom serializer class
    serializer_class = PasswordResetSerializer


class ConfirmEmailApi(ConfirmEmailView):

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()

        # check if the email is already verified
        if not confirmation.email_address.verified:
            # if the email is not verified verify the email
            confirmation.confirm(self.request)
            # return that the email verification was successfull
            return JsonResponse({
                "detail": "Email Verification successful"
            })
        # if the email was already verified return
        # a response to the user that the email was verified
        return JsonResponse({
            "detail": "Your Email was already verified.Try logging in."
        }, status=400)


class SocialLoginView(KnoxLoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class DRFAuthenticatedGraphQLView(GraphQLView):
    batch = True

    def parse_body(self, request):
        if isinstance(request, Request):
            return request.data
        return super(DRFAuthenticatedGraphQLView, self).parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(DRFAuthenticatedGraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((AllowAny,))(view)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
        view = api_view(["GET", "POST"])(view)
        return view
