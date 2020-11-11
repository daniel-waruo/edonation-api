from time import timezone

from django.db import models
from django.db.models import Sum
from django.utils import timezone

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
        products = Product.objects.get(
            campaign_products__donationproduct__in=donation_products
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
    """Track delivery of products after campaign is over """
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    state = models.CharField(
        choices=(
            ("pending", "Pending"),
            ("delivered", "Delivered")
        ),
        max_length=10,
        default="pending"
    )
    delivery_date = models.DateTimeField(null=True)


class DeliveryProduct(models.Model):
    """ Product to be delivered """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="delivery_products")
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="products")
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ("product", "delivery")
