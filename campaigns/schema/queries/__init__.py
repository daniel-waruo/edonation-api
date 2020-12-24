import graphene

from campaigns.models import Campaign, CampaignProduct
from products.models import Product
from products.schema.types import ProductType,filter_products
from donations.models import Donation
from django.db.models import Count,Sum
from campaigns.schema.types import (
    CampaignType,
    CampaignProductType,
    DonationDateType,
    CampaignCountType
)
from .campaigns_queries import Query as CampaignsQuery


class Query(CampaignsQuery,graphene.ObjectType,):
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

    donate_campaign = graphene.Field(
        CampaignType,
        id=graphene.ID(),
        slug=graphene.String()
    )

    def resolve_donate_campaign(self, info, **kwargs):
        slug = kwargs.get("slug")
        campaign = None
        if kwargs.get("id"):
            if Campaign.objects.filter(id=kwargs.get("id")).exists():
                campaign = Campaign.objects.get(id=kwargs.get("id"))
        if slug:
            if Campaign.objects.filter(slug=slug).exists():
                campaign = Campaign.objects.get(slug=slug)
        if campaign:
            if campaign.is_approved:
                return campaign
        return None

    campaign_product = graphene.Field(
        CampaignProductType,
        id=graphene.ID(),
        slug=graphene.String(),
        campaign_slug=graphene.String(),
    )

    def resolve_campaign_product(self, info, **kwargs):
        campaign_product_id = kwargs.get("id")
        campaign_product_slug = kwargs.get("slug")
        campaign_slug = kwargs.get("campaign_slug")
        if campaign_product_id:
            if CampaignProduct.objects.filter(id=campaign_product_id).exists():
                return CampaignProduct.objects.get(id=campaign_product_id)
        elif campaign_product_slug:
            if CampaignProduct.objects.filter(
                    campaign__slug=campaign_slug,
                    product__slug=campaign_product_slug).exists():
                return CampaignProduct.objects.get(
                    campaign__slug=campaign_slug,
                    product__slug=campaign_product_slug)
        return None

    add_products = graphene.List(
        ProductType,
        id=graphene.Int(required=True),
        query=graphene.String(),
        number=graphene.Int(),
        from_item=graphene.Int()
    )

    def resolve_add_products(self, info, **kwargs):
        if not Campaign.objects.filter(id=kwargs["id"], deleted=False):
            raise Exception("Invalid Campaign ID")
        campaign = Campaign.objects.get(id=kwargs["id"], deleted=False)
        product_ids = list(map(lambda p: p.product.id, campaign.products.all()))
        products = Product.objects.filter(deleted=False)
        products = products.exclude(id__in=product_ids)
        return filter_products(products,**kwargs)

    donations_by_date = graphene.List(DonationDateType)

    def resolve_donations_by_date(self: Campaign, info, **kwargs):
        donations = Donation.objects.filter(
            payment_status="success"
        ).extra({'date': "date(created_on)"}).values('date').annotate(number=Count('id'))
        return list(map(lambda x: DonationDateType(date=x["date"], number=x["number"]), donations))

    campaign_count  = graphene.Field(CampaignCountType)

    def resolve_campaign_count(self,info,**kwargs):
        return CampaignCountType()
