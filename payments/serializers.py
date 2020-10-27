import re

from django.core.validators import RegexValidator
from rest_framework import serializers

from cart.models import Cart
from donations.models import Donation
from .utils import pay_campaign_fee, pay_donation

phone_regex = re.compile('^(?:\+254)?(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$')


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
    donor_name = serializers.CharField()
    donor_phone = serializers.CharField(
        required=True,
        validators=[RegexValidator(phone_regex, message="Invalid Phone Number")]
    )
    donor_email = serializers.EmailField()
    campaign_slug = serializers.SlugField(required=False)

    def save(self, **kwargs):
        cart = Cart.objects.get_from_request(self.context["request"])
        donation = Donation.objects.create(
            cart=cart,
            **self.validated_data
        )

        return pay_donation(donation)
