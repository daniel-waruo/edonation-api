import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField

from campaigns.models import Campaign, CampaignProduct, CampaignProfile
from cart.models import Cart


@convert_django_field.register(ImageField)
def convert_field(field, registry=None):
    return graphene.String()


class CampaignType(DjangoObjectType):
    class Meta:
        model = Campaign


class CampaignProfileType(DjangoObjectType):
    class Meta:
        model = CampaignProfile


class CampaignProductType(DjangoObjectType):
    class Meta:
        model = CampaignProduct

    in_cart = graphene.Boolean()

    def resolve_in_cart(self: CampaignProduct, info):
        cart = Cart.objects.get_from_request(info.context)
        return cart.products.filter(id=self.id).exists()

