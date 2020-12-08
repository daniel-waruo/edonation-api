import graphene

from payments.models import DonationTransaction
from .types import DonationTransactionType


class Query(graphene.ObjectType):
    donation_transaction = graphene.Field(DonationTransactionType, id=graphene.ID(required=True))

    def resolve_donation_transaction(self, info, **kwargs):
        transaction_id = kwargs["id"]
        if not DonationTransaction.objects.filter(id=transaction_id).exists():
            return None
        return DonationTransaction.objects.get(id=transaction_id)
