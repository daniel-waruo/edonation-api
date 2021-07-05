import uuid

from django.conf import settings

from payments.models import (
    CampaignFeeTransaction,
    DonationTransaction,
    Transaction
)
from payments.stk import initiate_stk, check_stk_status


def pay_via_transaction(transaction: Transaction, callback_url):
    try:
        response = initiate_stk(
            phone_number=transaction.phone,
            amount=transaction.amount,
            transaction_id=transaction.id,
            callback_url=callback_url
        )
        if response.get('ResponseCode') == '0':
            transaction.set_pending(
                merchant_request_id=response['MerchantRequestID'],
                checkout_request_id=response['CheckoutRequestID']
            )
            return True, transaction
        transaction.set_fail(
            merchant_request_id=None,
            checkout_request_id=None,
            reason_failed=response.get('errorMessage')
        )
        return False, transaction
    except Exception as e:
        message = str(e.args)
        transaction.set_fail(
            merchant_request_id=None,
            checkout_request_id=None,
            reason_failed=message
        )
        return False, transaction


def pay_campaign_fee(phone, user):
    """ initiates payment of campaign fee
    Args:
        phone - phone number of the customer sending the money

    Returns:
        tuple(success_status,transaction) - returns a success message and the transaction
    """
    transaction = CampaignFeeTransaction.objects.create(
        amount=settings.CAMPAIGN_FEE,
        user=user,
        phone=phone
    )
    callback_url = f'{settings.CALLBACK_BASE_URL}/callback/campaign-fee'
    return pay_via_transaction(transaction, callback_url)


def pay_donation(donation):
    """ pay for the donation
    Args:
        donation - the donation to be paid for
    Returns:
        tuple(success_status,transaction) - returns a success message and the transaction
    """
    transaction = DonationTransaction.objects.create(donation)
    callback_url = f'{settings.CALLBACK_BASE_URL}/callback/donation-payment'
    return pay_via_transaction(transaction, callback_url)


"""
{
    'ResponseCode': '0', 
    'ResponseDescription': 'The service request has been accepted successsfully', 
    'MerchantRequestID': '6077-23902237-1', 
    'CheckoutRequestID': 'ws_CO_260620212203234583', 
    'ResultCode': '0', 
    'ResultDesc': 'The service request is processed successfully.'
}
"""


def update_transaction_status(transaction: Transaction):
    response = check_stk_status(
        checkout_transaction_id=transaction.checkout_request_id
    )
    response = dict(**response)
    response_code = response.get("ResultCode")
    if response_code is None:
        return transaction
    elif response_code != '0':
        merchant_request_id = response["MerchantRequestID"]
        checkout_request_id = response["CheckoutRequestID"]
        transaction.set_fail(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            reason_failed=response['ResponseDescription']
        )
        return transaction
    elif response_code == '0':
        merchant_request_id = response["MerchantRequestID"]
        checkout_request_id = response["CheckoutRequestID"]
        transaction.set_success(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            mpesa_code=uuid.uuid4()
        )
        return transaction
    return transaction
