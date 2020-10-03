import graphene

from campaigns.models import Campaign
from products.models import Product
from products.schema.types import ProductType
from .types import (
    CampaignType
)


class Query(graphene.ObjectType):
    campaign = graphene.Field(
        CampaignType,
        id=graphene.ID(),
        slug=graphene.String()
    )

    def resolve_campaign(self, info, **kwargs):
        slug = kwargs.get("slug")
        if kwargs.get("id"):
            if Campaign.objects.filter(id=kwargs.get("id")).exists():
                return Campaign.objects.get(id=kwargs.get("id"))
        if slug:
            if Campaign.objects.filter(slug=slug).exists():
                return Campaign.objects.get(slug=slug)
        return None

    campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(deleted=False)
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    add_products = graphene.List(ProductType, id=graphene.Int(required=True), query=graphene.String())

    def resolve_add_products(self, info, **kwargs):
        if not Campaign.objects.filter(id=kwargs["id"], deleted=False):
            raise Exception("Invalid Campaign ID")
        campaign = Campaign.objects.get(id=kwargs["id"], deleted=False)
        product_ids = list(map(lambda p: p.product.id, campaign.products.all()))
        products = Product.objects.filter(deleted=False)
        products = products.exclude(id__in=product_ids)
        if kwargs.get("query"):
            products = products.filter(name__icontains=kwargs.get("query"))
        return products
