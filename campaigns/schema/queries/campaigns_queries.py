import graphene

from campaigns.models import Campaign
from cart.models import Cart
from ..types import (
    CampaignType
)


def filter_campaigns(qs, query=None, number=None, from_item=None):
    """ This funtion is the one we will use to search and paginate campaigns
    Arguments:
        qs - the campaigns query set to be filtered
        query -  the query if available
        number - the number of items
        last_item - the position of the last item on the list
    """
    if query:
        qs = qs.filter(name__icontains=query)
    # if both parameters are provided
    if not (number is None or from_item is None):
        # get the number items from the last item to the number of items
        qs = qs[from_item:from_item + number]
    return qs


CampaignListQueryType = graphene.List(
    CampaignType,
    query=graphene.String(),
    number=graphene.Int(),
    from_item=graphene.Int()
)


class Query(graphene.ObjectType):
    campaigns = CampaignListQueryType

    def resolve_campaigns(self, info, **kwargs):
        """get all active non deleted campaigns"""
        qs = Campaign.objects.filter(deleted=False, is_active=True)
        return filter_campaigns(qs, **kwargs)

    valid_campaigns = CampaignListQueryType

    def resolve_valid_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(
            deleted=False,
            is_active=True,
            is_approved=True
        )
        return filter_campaigns(qs, **kwargs)

    cart_campaigns = CampaignListQueryType

    def resolve_cart_campaigns(self, info, **kwargs):
        cart = Cart.objects.get_from_request(info.context)
        qs = Campaign.objects.filter(
            deleted=False,
            is_active=True,
            is_approved=True,
            products__cart_products__cart=cart

        ).distinct()
        return filter_campaigns(qs, **kwargs)

    donated_campaigns = CampaignListQueryType

    def resolve_donated_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(
            deleted=False,
            is_active=True,
            is_approved=True,
            products__cart_products__cart__isnull=False
        )
        return filter_campaigns(qs, **kwargs)

    approved_campaigns = CampaignListQueryType

    def resolve_approved_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(
            deleted=False,
            is_active=True,
            is_approved=True
        )
        return filter_campaigns(qs, **kwargs)

    unapproved_campaigns = CampaignListQueryType

    def resolve_unapproved_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(
            deleted=False,
            is_active=True,
            is_approved=False
        )
        return filter_campaigns(qs, **kwargs)

    featured_campaigns = CampaignListQueryType

    def resolve_featured_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(
            deleted=False,
            is_active=True,
            is_featured=True
        )
        return filter_campaigns(qs, **kwargs)

    closed_campaigns = CampaignListQueryType

    def resolve_closed_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(delivery__isnull=False)
        return filter_campaigns(qs, **kwargs)

    pending_campaigns = CampaignListQueryType

    def resolve_pending_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(delivery__state="pending")
        return filter_campaigns(qs, **kwargs)

    processing_campaigns = CampaignListQueryType

    def resolve_processing_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(delivery__state="processing")
        return filter_campaigns(qs, **kwargs)

    ready_campaigns = CampaignListQueryType

    def resolve_ready_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(delivery__state="ready")
        return filter_campaigns(qs, **kwargs)

    delivered_campaigns = CampaignListQueryType

    def resolve_delivered_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(delivery__state="delivered")
        return filter_campaigns(qs, **kwargs)

    total_active_campaigns = graphene.Int()

    def resolve_total_active_campaigns(self, info, **kwargs):
        qs = Campaign.objects.filter(
            deleted=False,
            is_active=True,
            is_approved=True
        )
        return qs.count()
