from django.db import models
from campaigns.models import CampaignProduct
from cart.models import Cart, CartProduct


class DonationManager(models.Manager):
    def create(self, donor_phone, cart, donor_name=None, donor_email=None, campaign_slug=None):
        donation = super().create(
            donor_name=donor_name or "Anonymous",
            donor_phone=donor_phone,
            donor_email=donor_email,
            cart=cart,
            amount_paid=cart.total()
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
                quantity=cart_product.quantity,
                product_price=cart_product.product_total()
            )


class Donation(models.Model):
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    donor_name = models.CharField(max_length=50, null=True, blank=True)
    donor_phone = models.CharField(max_length=15)
    donor_email = models.EmailField(blank=True, null=True)
    TRANSACTION_STATE = (
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('success', 'Success')
    )
    payment_status = models.CharField(choices=TRANSACTION_STATE, max_length=7, default='pending')
    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, null=True)
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


class DonationProduct(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(CampaignProduct, on_delete=models.CASCADE, related_name="donation_products")
    product_price = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField(default=1)
    delivered = models.BooleanField(default=False)

    class Meta:
        unique_together = ('donation', 'product')
