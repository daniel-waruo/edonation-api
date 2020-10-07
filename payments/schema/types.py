import graphene
from graphene_django.types import DjangoObjectType

from payments.models import CampaignFeeTransaction


class CampaignFeeTransactionType(DjangoObjectType):
    success_status = graphene.Boolean()

    def resolve_success_status(self: CampaignFeeTransaction, info):
        return self.is_success

    class Meta:
        model = CampaignFeeTransaction
        exclude = ['transaction_id']
