import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField

from campaigns.models import Campaign, CampaignProduct


@convert_django_field.register(ImageField)
def convert_field(field, registry=None):
    return graphene.String()


class CampaignType(DjangoObjectType):
    class Meta:
        model = Campaign


class CampaignProductType(DjangoObjectType):
    class Meta:
        model = CampaignProduct
