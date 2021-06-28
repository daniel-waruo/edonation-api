from django.contrib.auth import get_user_model
from django.db import models

from cart.models import CartProduct
from donations.models import Donation

User = get_user_model()


class Transaction(models.Model):
    merchant_request_id = models.CharField(max_length=64, null=True, unique=True)
    checkout_request_id = models.CharField(max_length=64, null=True, unique=True)
    mpesa_code = models.CharField(max_length=64, null=True, unique=True)
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

    def set_pending(self, merchant_request_id, checkout_request_id):
        self.merchant_request_id = merchant_request_id
        self.checkout_request_id = checkout_request_id
        self.state = 'pending'
        self.save()

    def set_fail(self, merchant_request_id, checkout_request_id, reason_failed):
        self.state = 'failed'
        assert self.checkout_request_id == checkout_request_id
        assert self.merchant_request_id == merchant_request_id
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

    def set_success(self, merchant_request_id, checkout_request_id, mpesa_code):
        self.mpesa_code = mpesa_code
        self.state = 'success'
        assert self.checkout_request_id == checkout_request_id
        assert self.merchant_request_id == merchant_request_id
        self.save()
        # set the campaign profile as paid
        campaign_profile = self.user.campaign_profile
        campaign_profile.paid = True
        campaign_profile.save()


class DonationTransactionManager(models.Manager):
    def create(self, donation):
        return super().create(
            amount=donation.amount,
            donation=donation,
            phone=donation.donor_phone,
        )


class DonationTransaction(Transaction):
    donation = models.OneToOneField(
        Donation,
        on_delete=models.CASCADE,
        related_name="transaction"
    )

    objects = DonationTransactionManager()

    def set_fail(self, merchant_request_id, checkout_request_id, reason_failed):
        super(DonationTransaction, self).set_fail(
            merchant_request_id,
            checkout_request_id,
            reason_failed
        )
        self.donation.set_fail()

    def set_success(self, merchant_request_id, checkout_request_id, mpesa_code):
        self.mpesa_code = mpesa_code
        self.state = 'success'
        assert self.checkout_request_id == checkout_request_id
        assert self.merchant_request_id == merchant_request_id
        self.save()
        # set donation as successful
        self.donation.set_success()
        # remove all donated products from the cart
        CartProduct.objects.filter(
            product__donation_products__in=self.donation.products.all()
        ).delete()
