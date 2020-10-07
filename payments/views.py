import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from payments.models import CampaignFeeTransaction


@csrf_exempt
def notification_callback(request):
    data = json.loads(request.body)
    # get metadata
    meta_data = data['requestMetadata']
    if meta_data['type'] == 'CampaignFeeTransaction':
        return campaign_fee_callback(data)
    return HttpResponse(status=400, content="Invalid Request Data")


def campaign_fee_callback(data):
    """ saves the successful transaction """
    # get AT transaction id
    at_transaction_id = data['transactionId']
    meta_data = data['requestMetadata']

    transaction_id = meta_data["transaction_id"]
    if not CampaignFeeTransaction.objects.filter(id=transaction_id).exists():
        return HttpResponse("Subscription transaction is not valid")
    transaction = CampaignFeeTransaction.objects.get(id=transaction_id)
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
