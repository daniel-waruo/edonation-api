from rest_framework import serializers

from campaigns.models import Campaign, CampaignProduct


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["name", "description", "image", "owner"]


class CampaignProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignProduct
        fields = "__all__"
