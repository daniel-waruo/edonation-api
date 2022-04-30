import re

from django.core.validators import RegexValidator
from rest_framework import serializers

from cart.models import Cart
from donations.models import Donation
from .utils import pay_campaign_fee, pay_donation

phone_regex = re.compile('^254([0-9]{9})$')


class CampaignFeePaymentSerializer(serializers.Serializer):
    phone = serializers.CharField(
        required=True,
        validators=[RegexValidator(phone_regex, message="Invalid Phone Number")]
    )

    def save(self, **kwarg):
        phone = self.validated_data['phone']
        user = self.context['request'].user
        return pay_campaign_fee(phone, user)


class DonationPaymentSerializer(serializers.Serializer):
    donor_name = serializers.CharField(required=False, allow_blank=True)
    donor_phone = serializers.CharField(
        required=True,
        validators=[RegexValidator(phone_regex, message="Invalid Phone Number")]
    )
    donor_email = serializers.EmailField(required=False, allow_blank=True)
    campaign_slug = serializers.SlugField(required=True)

    def save(self, **kwargs):
        cart = Cart.objects.get_from_request(self.context["request"])
        donation = Donation.objects.create(
            cart=cart,
            **self.validated_data
        )

        return pay_donation(donation)
