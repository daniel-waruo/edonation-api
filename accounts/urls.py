from allauth.account.views import email_verification_sent
from django.urls import path
from rest_auth.registration.views import VerifyEmailView

from accounts.views import (
    ConfirmEmailApi,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
PasswordResetResendView
)

urlpatterns = [
    # REGISTER URLS #
    # url for account confirmation using the link sent in the email
    path('register/account-confirm-email/<str:key>', ConfirmEmailApi.as_view(), name='account_confirm_email'),
    # url for verifying an email
    path('register/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    # url for informing the user that the verification in sent
    path("register/confirm-email/", email_verification_sent, name="account_email_verification_sent"),

    # PASSWORD URLS #,
    path('reset-resend/<uidb64>/', PasswordResetResendView.as_view(), name='password_reset_resend'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
