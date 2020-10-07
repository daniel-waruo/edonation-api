import africastalking
from africastalking import PaymentService
from django.conf import settings

# set payment provider
provider = 'Athena' if settings.AT_USERNAME == 'sandbox' else 'Mpesa'

africastalking.initialize(
    username=settings.AT_USERNAME,
    api_key=settings.AT_API_KEY
)

pay: PaymentService = africastalking.Payment

payment_product = settings.AT_PAYMENT_PRODUCT


def pay_campaign_fee(phone, user):
    """ request's payment from africa'stalking API
    Args:
        phone - phone number of the customer sending the money

    Returns:
        tuple(success_status,transaction) - returns a success message and the transaction
    """
    from payments.models import CampaignFeeTransaction
    paid_amount = settings.CAMPAIGN_FEE
    transaction = CampaignFeeTransaction.objects.create(
        amount=paid_amount,
        user=user,
        phone=phone
    )

    try:
        response = pay.mobile_checkout(
            product_name=payment_product,
            phone_number=phone,
            currency_code="KES",
            amount=paid_amount,
            metadata={
                'type': 'CampaignFeeTransaction',
                'transaction_id': str(transaction.id)
            }
        )
        if response.get('status') == 'PendingConfirmation':
            transaction.set_pending(response['transactionId'])
            return True, transaction
        transaction.set_fail(
            transaction_id=response.get('transactionId'),
            reason_failed=response.get('description')
        )
        return False, transaction
    except Exception as e:
        message = str(e.args)
        transaction.set_fail(
            transaction_id=None,
            reason_failed=message
        )
        return False, transaction
