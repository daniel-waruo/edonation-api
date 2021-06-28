from django.urls import path
from .views import campaign_fee_callback,donation_payment_callback

urlpatterns = [
    path('campaign-fee', campaign_fee_callback),
    path('donation-payment', donation_payment_callback),
]
