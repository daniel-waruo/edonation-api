import graphene
from django.db.models import Sum, F, FloatField
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import FileField

from deliveries.models import Delivery, DeliveryProduct
from donations.models import DonationProduct, Donation


@convert_django_field.register(FileField)
def convert_field(field, registry=None):
    return graphene.String()


class DeliveryType(DjangoObjectType):
    total_donated = graphene.Float()

    def resolve_total_donated(self: Delivery, info):
        donation_products = DonationProduct.objects.filter(product__campaign__delivery=self)
        return donation_products.aggregate(
            donation_amount=Sum(F("quantity") * F("product_price"), output_field=FloatField())
        )["donation_amount"] or 0

    class Meta:
        model = Delivery


class DeliveryProductType(DjangoObjectType):
    total_donated = graphene.Float()

    def resolve_total_donated(self: DeliveryProduct, info):
        donation_products = DonationProduct.objects.filter(
            product__product__delivery_products=self
        )
        return donation_products.aggregate(
            donation_amount=Sum(F("quantity") * F("product_price"), output_field=FloatField())
        )["donation_amount"] or 0

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
