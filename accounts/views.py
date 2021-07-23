from allauth.account import app_settings
from allauth.account.views import ConfirmEmailView
from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetCompleteView as BasePasswordResetCompleteView, INTERNAL_RESET_SESSION_TOKEN, UserModel
)
from django.http import Http404
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import (AllowAny)
from rest_framework.request import Request
from rest_framework.settings import api_settings

from accounts.forms import PasswordResetForm


class ConfirmEmailApi(ConfirmEmailView):
    template_name = "account/email_confirm.html"

    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            if app_settings.CONFIRM_EMAIL_ON_GET:
                return self.post(*args, **kwargs)
        except Http404:
            self.object = None
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        # check if the email is already verified
        if not confirmation.email_address.verified:
            # if the email is not verified verify the email
            confirmation.confirm(self.request)
            # return that the email verification was successful
            return JsonResponse({
                "detail": "Email Verification successful"
            })
        # if the email was already verified return
        # a response to the user that the email was verified
        return JsonResponse({
            "detail": "Your Email was already verified.Try logging in."
        }, status=400)


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

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except Exception:
            user = None
        return user

    def get(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs
        user = self.get_user(kwargs['uidb64'])
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
