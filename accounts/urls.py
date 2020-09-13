from allauth.account.views import email_verification_sent, password_reset_from_key, password_reset_from_key_done
from django.urls import path, re_path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (
    LogoutView,
    PasswordChangeView,
)

from accounts.views import (
    KnoxRegisterView,
    PasswordResetView,
    ConfirmEmailApi
)

urlpatterns = [
    # url for user logout
    path('logout/', LogoutView.as_view(), name='rest_logout'),

    # REGISTER URLS #
    # url for registering new users
    path('register/', KnoxRegisterView.as_view(), name='rest_register'),
    # url for account confirmation using the link sent in the email
    path('register/account-confirm-email/<str:key>', ConfirmEmailApi.as_view(), name='account_confirm_email'),
    # url for verifying an email
    path('register/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    # url for informing the user that the verification in sent
    path("register/confirm-email/", email_verification_sent, name="account_email_verification_sent"),

    # PASSWORD URLS #
    # url for sending reset password links to the email
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    # url link used for resetting user password from the link sent in the email
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
            password_reset_from_key,
            name="account_reset_password_from_key"),
    # url show password reset done
    path("password/reset/key/done/", password_reset_from_key_done,
         name="account_reset_password_from_key_done"),
    # url for handling password change
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),

]
