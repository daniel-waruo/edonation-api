import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from payments.models import CampaignFeeTransaction, DonationTransaction


@csrf_exempt
def campaign_fee_callback(request):
    """ processes the mpesa api callback """
    # get data from request
    data = json.loads(request.body)
    # africa's talking transaction id
    at_transaction_id = data['transactionId']
    # get the metadata we sent with the request
    meta_data = data['requestMetadata']
    # get the campaign fee transaction id
    transaction_id = meta_data["transaction_id"]

    if not CampaignFeeTransaction.objects.filter(id=transaction_id).exists():
        return HttpResponse("Campaign transaction is not valid")
    # get instance of the campaign fee transaction
    transaction = CampaignFeeTransaction.objects.get(id=transaction_id)
    # only process pending transactions
    if transaction.is_pending:
        # check if the transaction was successful
        if data.get('status') == 'Success':
            transaction_fee = data['transactionFee']
            provider_fee = data['providerFee']
            # get the numeric fee values
            transaction_fee = transaction_fee.split()[1]
            provider_fee = provider_fee.split()[1]
            total_fee = float(transaction_fee) + float(provider_fee)
            transaction.set_success(
                mpesa_code=data['providerRefId'],
                transaction_id=at_transaction_id,
                transaction_cost=total_fee
            )
            return HttpResponse()
        # if the request is not successful set status as failed
        # and save the reason why in the database
        transaction.set_fail(
            transaction_id=at_transaction_id,
            reason_failed=data.get('description')
        )
    return HttpResponse()


@csrf_exempt
def donation_payment_callback(request):
    """processes the africa's talking callback
     Arguments:
         data - data sent by africa's talking as a callback
     Returns:
         HTTPResponse - a 200 response to make sure that africa's talking stops sending callback
     """
    data = json.loads(request.body)
    # get AT transaction id
    # africa's talking transaction id
    at_transaction_id = data['transactionId']
    # get the metadata we sent with the request
    meta_data = data['requestMetadata']
    # get the campaign fee transaction id
    transaction_id = meta_data["transaction_id"]

    if not DonationTransaction.objects.filter(id=transaction_id).exists():
        return HttpResponse("Donation transaction is not valid")
    # get instance of the campaign fee transaction
    transaction = DonationTransaction.objects.get(id=transaction_id)
    # only process pending transactions
    if transaction.is_pending:
        # check if the transaction was successful
        if data.get('status') == 'Success':
            if transaction.is_pending:
                transaction_fee = data['transactionFee']
                provider_fee = data['providerFee']
                # get the numeric fee values
                transaction_fee = transaction_fee.split()[1]
                provider_fee = provider_fee.split()[1]
                total_fee = float(transaction_fee) + float(provider_fee)
                transaction.set_success(
                    mpesa_code=data['providerRefId'],
                    transaction_id=at_transaction_id,
                    transaction_cost=total_fee
                )
            return HttpResponse()
        transaction.set_fail(
            transaction_id=at_transaction_id,
            reason_failed=data.get('description')
        )
    return HttpResponse()
