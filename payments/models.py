from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Transaction(models.Model):
    transaction_id = models.TextField(unique=True, null=True)
    mpesa_code = models.CharField(max_length=200, null=True, unique=True)
    phone = models.CharField(max_length=30)
    reason_failed = models.TextField(null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    transaction_cost = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    transaction_date = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    TRANSACTION_STATE = (
        ('requested', 'Payment Requested'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('success', 'Success')
    )
    state = models.CharField(choices=TRANSACTION_STATE, max_length=10, default='requested')

    @property
    def is_requested(self):
        return self.state == 'requested'

    @property
    def is_success(self):
        return self.state == 'success'

    @property
    def is_fail(self):
        return self.state == 'failed'

    @property
    def is_pending(self):
        return self.state == 'pending'

    def set_pending(self, transaction_id):
        self.transaction_id = transaction_id
        self.state = 'pending'
        self.save()

    def set_fail(self, transaction_id, reason_failed):
        self.state = 'failed'
        self.transaction_id = transaction_id
        self.reason_failed = reason_failed
        self.save()

    def set_success(self, **kwargs):
        raise NotImplementedError("Implement set success")

    class Meta:
        abstract = True


class CampaignFeeTransactionManager(models.Manager):
    def create(self, amount: float, user, phone: str):
        return super().create(
            amount=amount,
            user=user,
            phone=phone,
        )


class CampaignFeeTransaction(Transaction):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='campaign_fee_transactions'
    )

    objects = CampaignFeeTransactionManager()

    def set_success(self, transaction_id, mpesa_code, transaction_cost):
        self.mpesa_code = mpesa_code
        self.state = 'success'
        self.transaction_id = transaction_id
        # the amount of money it cost us to
        # make the transaction
        self.transaction_cost = transaction_cost
        self.save()
        # set the campaign profile as paid
        campaign_profile = self.user.campaign_profile
        campaign_profile.paid = True
        campaign_profile.save()