from time import timezone

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from pyuploadcare.dj.models import FileField

from campaigns.models import Campaign
from donations.models import DonationProduct
from products.models import Product


class DeliveryManager(models.Manager):
    def delivery_from_campaign(self, campaign: Campaign):
        # make campaign inactive
        campaign.is_active = False
        # set end date as the current date
        campaign.end_date = timezone.now()
        # get all the products donated and the number they are donated
        donation_products = DonationProduct.objects.filter(product__campaign=campaign)
        products = Product.objects.filter(
            campaign_products__donation_products__in=donation_products
        ).distinct()
        # create a delivery
        delivery = self.create(
            campaign=campaign
        )
        # use this list of products to create a list of delivery products
        for product in products:
            product_donations = product.donation_products.filter(
                product__campaign=campaign
            )
            number_donated = 0
            if product_donations:
                number_donated = product_donations.aggregate(
                    number_donated=Sum("quantity")
                )["number_donated"]
            # create a delivery product
            DeliveryProduct.objects.create(
                delivery=delivery,
                product=product,
                number=number_donated
            )
        campaign.save()
        pass


class Delivery(models.Model):
    """ Track delivery of products after campaign is over
    campaign - the campaign whose delivery we are making
    state - the state of the delivery whether it is pending delivery or it is delivered
    delivery_form - the form signed by the campaign creator once it is delivered
    delivery_date - the date the delivery was made
    """
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    state = models.CharField(
        choices=(
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("ready", "Ready"),
            ("delivered", "Delivered")
        ),
        max_length=10,
        default="pending"
    )
    delivery_form = FileField(null=True)
    delivery_date = models.DateTimeField(null=True)

    objects = DeliveryManager()

    def next_state(self):
        new_state = "processing"
        old_state = self.state
        if old_state == "processing":
            new_state = "ready"
        elif old_state == "ready":
            new_state = "delivered"
        if old_state == "delivered":
            new_state = old_state
        self.state = new_state
        self.save()


class DeliveryProduct(models.Model):
    """ Product to be delivered """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="delivery_products")
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="products")
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ("product", "delivery")
