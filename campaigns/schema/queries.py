import graphene

from campaigns.models import Campaign, CampaignProduct
from products.models import Product
from products.schema.types import ProductType
from donations.models import Donation
from django.db.models import Count,Sum
from .types import (
    CampaignType, CampaignProductType,DonationDateType
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

    campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(deleted=False, is_active=True)
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    donate_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_donate_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(
            deleted=False,
            is_active=True,
            is_approved=True
        )
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns
        
    total_active_campaigns = graphene.Int()

    def resolve_total_active_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(
            deleted=False,
            is_active=True,
            is_approved=True
        )
        return campaigns.count()

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

    approved_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_approved_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(deleted=False, is_active=True,is_approved=True)
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    unapproved_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_unapproved_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(deleted=False, is_active=True,is_approved=False)
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    featured_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_featured_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(deleted=False, is_active=True,is_featured=True)
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    closed_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_closed_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(delivery__isnull=False)
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    pending_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_pending_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(delivery__state="pending")
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    processing_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_processing_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(delivery__state="processing")
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    ready_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_ready_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(delivery__state="ready")
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    delivered_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_delivered_campaigns(self, info, **kwargs):
        campaigns = Campaign.objects.filter(delivery__state="delivered")
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns


    donations_by_date = graphene.List(DonationDateType)

    def resolve_donations_by_date(self: Campaign, info, **kwargs):
        donations = Donation.objects.filter(
            payment_status="success"
        ).extra({'date': "date(created_on)"}).values('date').annotate(number=Count('id'))
        return list(map(lambda x: DonationDateType(date=x["date"], number=x["number"]), donations))
