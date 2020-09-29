from rest_framework import serializers

from campaigns.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["name", "description", "image", "owner"]
