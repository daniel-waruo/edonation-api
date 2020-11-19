import graphene

from deliveries.schema.types import DeliveryType, DeliveryCountType


class Query(graphene.ObjectType):
    delivery = graphene.Field(DeliveryType)

    delivery_count = graphene.Field(DeliveryCountType)

    def resolve_delivery_count(self, info, **kwargs):
        return DeliveryCountType()
