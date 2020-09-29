import graphene

from campaigns.models import Campaign
from .types import (
    CampaignType
)


class Query(graphene.ObjectType):
    campaign = graphene.Field(
        CampaignType,
        id=graphene.ID(),
        slug=graphene.String()
    )

    def resolve_campaign(self, info, id=None, slug=None):
        # check if there is an id specified
        if id:
            if Campaign.objects.filter(id=id).exists():
                return Campaign.objects.get(id=id)
        if slug:
            if Campaign.objects.filter(slug=slug).exists():
                return Campaign.objects.get(slug=slug)
        return None

    campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_campaigns(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return None
        return user.campaigns.all()
