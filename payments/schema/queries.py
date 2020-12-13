import graphene

from payments.models import DonationTransaction
from .types import DonationTransactionType,TransactionDateType
from django.db.models import Sum

class Query(graphene.ObjectType):
    donation_transaction = graphene.Field(DonationTransactionType, id=graphene.ID(required=True))

    def resolve_donation_transaction(self, info, **kwargs):
        transaction_id = kwargs["id"]
        if not DonationTransaction.objects.filter(id=transaction_id).exists():
            return None
        return DonationTransaction.objects.get(id=transaction_id)

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
        return total_income
