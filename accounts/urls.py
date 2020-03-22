from allauth.account.views import password_reset_from_key
from django.urls import path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
)

from accounts.views import GoogleLogin
from accounts.views import KnoxRegisterView, ConfirmEmailApi
from accounts.views import PasswordResetView, KnoxLoginView

urlpatterns = [
    # url for user login
    path('login/', KnoxLoginView.as_view(), name='rest_login'),
    # url for user logout
    path('logout/', LogoutView.as_view(), name='rest_logout'),

    # url for registering new users
    path('register/', KnoxRegisterView.as_view(), name='rest_register'),
    # url for verifying email is valid
    path('register/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    # url for account confirmation using the link sent in the email
    path('register/account-confirm-email/<str:key>', ConfirmEmailApi.as_view(), name='account_confirm_email'),

    # url link used for resetting user password from the link sent in the email
    path(
        "password/reset/key/<uidb36>-<key>/",
        password_reset_from_key,
        name="account_reset_password_from_key"
    ),

    # PASSWORD URLS #
    # url for sending reset password links to the email
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    # url for confirming password reset links send to the email
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    # url for handling password change
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),

    # social login urls
    path('social/google/', GoogleLogin.as_view(), name='g_login'),

]
