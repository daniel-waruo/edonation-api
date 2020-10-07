import graphene

from accounts.schema.types import Error, errors_to_graphene
from payments.serializers import CampaignFeePaymentSerializer
from .types import CampaignFeeTransactionType


class PayCampaignFeeMutation(graphene.Mutation):
    """ Requests for payment subscription
    Args:
        success - whether the payment was successfull or not
        errors - errors that may have occurred in the process
    """
    success = graphene.Boolean()
    transaction = graphene.Field(CampaignFeeTransactionType)
    errors = graphene.List(Error)

    class Arguments:
        phone = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        """ Mutation that either returns a success boolean value or some errors"""
        serializer = CampaignFeePaymentSerializer(
            context={'request': info.context},
            data=kwargs
        )
        if serializer.is_valid():
            success_status, transaction = serializer.save()
            if success_status:
                return PayCampaignFeeMutation(
                    success=success_status,
                    transaction=transaction
                )
            return PayCampaignFeeMutation(
                success=False,
                errors=[Error(
                    field='non_field_errors',
                    errors=[f"{transaction.reason_failed}"]
                )]
            )
        return PayCampaignFeeMutation(
            errors=errors_to_graphene(serializer.errors)
        )


class Mutation(graphene.ObjectType):
    pay_campaign_fee = PayCampaignFeeMutation.Field()
