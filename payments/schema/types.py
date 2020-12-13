import graphene
from graphene_django.types import DjangoObjectType

from payments.models import CampaignFeeTransaction, DonationTransaction
from campaigns.schema.types import CampaignType
from campaigns.models import Campaign

class TransactionDateType(graphene.ObjectType):
    date = graphene.Date()
    amount = graphene.Float()
    
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

    campaigns  = graphene.List(CampaignType)


    def resolve_campaigns(self,info):
        campaigns = Campaign.objects.filter(
           products__donation_products__donation=self.donation
        ).distinct()
        return campaigns
