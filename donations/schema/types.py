from graphene_django import DjangoObjectType

from donations.models import Donation, DonationProduct


class DonationType(DjangoObjectType):
    class Meta:
        model = Donation


class DonationProductType(DjangoObjectType):
    class Meta:
        model = DonationProduct
