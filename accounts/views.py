from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetCompleteView as BasePasswordResetCompleteView, INTERNAL_RESET_SESSION_TOKEN, UserModel
)
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import (AllowAny)
from rest_framework.request import Request
from rest_framework.settings import api_settings

from accounts.forms import PasswordResetForm
from accounts.models import User
from accounts.tokens import AccountConfirmationTokenGenerator
from accounts.utils import send_confirmation_email


def get_user_from_uid(uidb64):
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except Exception:
        user = None
    return user


class ConfirmEmailApi(TemplateView):
    template_name = "pg_account/email_confirm.html"
    token_generator = AccountConfirmationTokenGenerator()

    def get(self, *args, **kwargs):
        # get user from uidb64
        assert 'uidb64' in kwargs and 'token' in kwargs
        user: User = get_user_from_uid(kwargs['uidb64'])
        # authenticate token against generator
        validlink = self.token_generator.check_token(user, kwargs['token'])
        # return valid context
        context = {
            "validlink": validlink,
            "user": user,
            "uid": kwargs['uidb64'],
            "token": kwargs['token']
        }
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs
        # check if the email is already verified
        # get user from uuid
        user: User = get_user_from_uid(kwargs['uidb64'])
        validlink = self.token_generator.check_token(user, kwargs['token'])
        if not validlink:
            return JsonResponse({
                "detail": "Invalid Confirmation Link"
            }, status=400)
        if not user.email_confirmed:
            # if the email is not verified verify the email
            user.email_confirmed = True
            user.save()
            # return that the email verification was successful
            return JsonResponse({
                "detail": "Email Verification successful"
            })
        # if the email was already verified return
        # a response to the user that the email was verified
        return JsonResponse({
            "detail": "Your Email was already verified.Try logging in."
        }, status=400)


class ConfirmResendView(TemplateView):
    template_name = 'pg_account/email_confirm_resend.html'

    def get(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs
        user = get_user_from_uid(kwargs['uidb64'])
        send_confirmation_email(user)
        return super().get(request, *args, **kwargs)


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name = 'pg_account/password_reset.html'

    def dispatch(self, *args, **kwargs):
        self.uid = kwargs["uidb64"]
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        return self.render_to_response(
            context={
                "form": None,
                "validlink": True
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uid"] = self.uid
        return context


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    pass


class PasswordResetResendView(TemplateView):
    template_name = 'pg_account/password_reset_resend.html'

    def get(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs
        user = get_user_from_uid(kwargs['uidb64'])
        form = PasswordResetForm({"email": user.email})
        form.is_valid()
        form.save()
        return super().get(request, *args, **kwargs)


class DRFAuthenticatedGraphQLView(GraphQLView):
    batch = False

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
