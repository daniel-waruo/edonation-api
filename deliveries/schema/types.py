import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import FileField

from deliveries.models import Delivery, DeliveryProduct


@convert_django_field.register(FileField)
def convert_field(field, registry=None):
    return graphene.String()


class DeliveryType(DjangoObjectType):
    class Meta:
        model = Delivery


class DeliveryProductType(DjangoObjectType):
    class Meta:
        model = DeliveryProduct
