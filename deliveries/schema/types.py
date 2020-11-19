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


class DeliveryCountType(graphene.ObjectType):
    all = graphene.Int()

    def resolve_all(self, info):
        return Delivery.objects.all().count()

    pending = graphene.Int()

    def resolve_pending(self, info):
        deliveries = Delivery.objects.filter(state="pending")
        return deliveries.count()

    processing = graphene.Int()

    def resolve_processing(self, info):
        deliveries = Delivery.objects.filter(state="processing")
        return deliveries.count()

    ready = graphene.Int()

    def resolve_ready(self, info):
        deliveries = Delivery.objects.filter(state="ready")
        return deliveries.count()

    delivered = graphene.Int()

    def resolve_delivered(self, info):
        deliveries = Delivery.objects.filter(state="delivered")
        return deliveries.count()
