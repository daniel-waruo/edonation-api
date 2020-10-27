import graphene
from graphene_django.types import DjangoObjectType

from payments.models import CampaignFeeTransaction, DonationTransaction


class CampaignFeeTransactionType(DjangoObjectType):
    success_status = graphene.Boolean()

    def resolve_success_status(self: CampaignFeeTransaction, info):
        return self.is_success

    class Meta:
        model = CampaignFeeTransaction
        exclude = ['transaction_id']


class DonationTransactionType(DjangoObjectType):
    success_status = graphene.Boolean()

    def resolve_success_status(self: DonationTransaction, info):
        return self.is_success

    class Meta:
        model = DonationTransaction
        exclude = ['transaction_id']
