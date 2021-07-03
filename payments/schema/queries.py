import graphene
from django.db.models import Sum

from payments.models import DonationTransaction, CampaignFeeTransaction
from payments.utils import update_transaction_status
from .types import DonationTransactionType, TransactionDateType, CampaignFeeTransactionType


class Query(graphene.ObjectType):
    campaign_fee_transaction = graphene.Field(CampaignFeeTransactionType, id=graphene.ID(required=True))

    def resolve_campaign_fee_transaction(self, info, **kwargs):
        transaction_id = kwargs["id"]
        if not CampaignFeeTransaction.objects.filter(id=transaction_id).exists():
            return None
        transaction = CampaignFeeTransaction.objects.get(id=transaction_id)
        if transaction.is_pending:
            transaction = update_transaction_status(transaction)
        return transaction

    donation_transaction = graphene.Field(DonationTransactionType, id=graphene.ID(required=True))

    def resolve_donation_transaction(self, info, **kwargs):
        transaction_id = kwargs["id"]
        if not DonationTransaction.objects.filter(id=transaction_id).exists():
            return None
        transaction = DonationTransaction.objects.get(id=transaction_id)
        if transaction.is_pending:
            transaction = update_transaction_status(transaction)
        return transaction

    income_by_date = graphene.List(TransactionDateType)

    def resolve_income_by_date(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return None
        donations = DonationTransaction.objects.filter(
            state="success"
        ).extra({'date': "date(created_on)"}).values('date').annotate(amount=Sum('amount'))
        return list(map(lambda x: TransactionDateType(date=x["date"], amount=x["amount"]), donations))

    total_income = graphene.Float()

    def resolve_total_income(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return None
        total_income = DonationTransaction.objects.filter(
            state="success"
        ).aggregate(amount=Sum('amount'))["amount"]
        return total_income or 0
