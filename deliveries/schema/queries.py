import graphene

from deliveries.schema.types import DeliveryType


class Query(graphene.ObjectType):
    delivery = graphene.Field(DeliveryType)
