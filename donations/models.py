from django.db import models
from django.db.models import Sum, F, FloatField

from campaigns.models import CampaignProduct
from cart.models import Cart, CartProduct


class DonationManager(models.Manager):
    def create(self, donor_phone, cart, donor_name=None, donor_email=None, campaign_slug=None):
        donation = super().create(
            donor_name=donor_name,
            donor_phone=donor_phone,
            donor_email=donor_email,
            cart=cart
        )
        cart_products = cart.products.all()
        if campaign_slug:
            cart_products = cart_products.filter(
                product__campaign__slug=campaign_slug
            )
        # create donation products
        self.cart_to_donation(donation, cart_products)
        return donation

    def cart_to_donation(self, donation, cart_products):
        for cart_product in cart_products:
            DonationProduct.objects.create(
                product=cart_product.product,
                donation=donation,
                quantity=cart_product.quantity
            )


class Donation(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    donor_name = models.CharField(max_length=50, null=True)
    donor_phone = models.CharField(max_length=15)
    donor_email = models.EmailField(null=True)
    TRANSACTION_STATE = (
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('success', 'Success')
    )
    payment_status = models.CharField(choices=TRANSACTION_STATE, max_length=7, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)
    objects = DonationManager()

    @property
    def is_paid(self):
        return self.payment_status == "success"

    def set_success(self):
        self.payment_status = "success"
        self.save()

    def set_fail(self):
        self.payment_status = "failed"
        self.save()

    @property
    def amount(self):
        """get the total price value of items in the cart """
        if self.products.all().exists():
            total = self.products.aggregate(
                donation_amount=Sum(F("quantity") * F("product__product__price"), output_field=FloatField())
            )["donation_amount"]
            return total
        return 0


class DonationProduct(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(CampaignProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('donation', 'product')
