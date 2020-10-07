import re

from django.core.validators import RegexValidator
from rest_framework import serializers

from .utils import pay_campaign_fee

phone_regex = re.compile('^(?:\+254)?(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$')


class CampaignFeePaymentSerializer(serializers.Serializer):
    phone = serializers.CharField(
        required=True,
        validators=[RegexValidator(phone_regex, message="Invalid Phone Number")]
    )

    def save(self, **kwargs):
        phone = self.validated_data['phone']
        user = self.context['request'].user
        return pay_campaign_fee(phone, user)
