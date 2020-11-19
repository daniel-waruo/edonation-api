import graphene

from accounts.schema.types import Error
from deliveries.models import Delivery


class NextDeliveryState(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        if not Delivery.objects.filter(campaign_id=kwargs["id"]).exists():
            return NextDeliveryState(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid Campaign ID"]
                    )
                ],
            )
        delivery = Delivery.objects.get(campaign_id=kwargs["id"])
        delivery.next_state()
        return NextDeliveryState(success=True)


class Mutation(graphene.ObjectType):
    next_delivery_state = NextDeliveryState.Field()
