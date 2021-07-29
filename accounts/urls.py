from django.urls import path

from accounts.views import (
    ConfirmResendView,
    ConfirmEmailApi,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetResendView
)

urlpatterns = [
    # EMAIL CONFIRMATION URLS
    path('confirm/<uidb64>/<token>/', ConfirmEmailApi.as_view(), name='confirm_email'),
    path('confirm-resend/<uidb64>/', ConfirmResendView.as_view(), name='resend_confirm_email'),
    # PASSWORD RESET URLS
    path('reset-resend/<uidb64>/', PasswordResetResendView.as_view(), name='password_reset_resend'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
