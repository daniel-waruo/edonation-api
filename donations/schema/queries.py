import graphene

from donations.models import Donation, DonationProduct
from .types import DonationType, DonationProductType


class Query(graphene.ObjectType):
    donation = graphene.Field(DonationType, id=graphene.ID(required=True))

    def resolve_donation(self, info, **kwargs):
        donation_id = kwargs["id"]
        if not Donation.objects.filter(id=donation_id).exists():
            return None
        return Donation.objects.get(id=donation_id)

    donation_products = graphene.List(DonationProductType, all=graphene.Boolean())

    def resolve_donation_products(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return None
        get_all = kwargs.get("all", False)
        donation_products = DonationProduct.objects.filter(product__campaign__owner=user)
        if get_all:
            return donation_products
        return donation_products.filter(donation__payment_status="success")

    total_donated = graphene.Int()

    def resolve_total_donated(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return None
        return Donation.objects.filter(payment_status="success").count()
