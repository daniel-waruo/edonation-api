from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from pyuploadcare import File
from pyuploadcare.dj.models import ImageField

from products.models import Product

User = get_user_model()


class Campaign(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="campaigns")
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True)
    image = ImageField(null=True)
    is_approved = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def complete(self):
        from deliveries.models import Delivery
        # create delivery from campaign
        self.is_active = False
        Delivery.objects.delivery_from_campaign(self)
        self.save()


@receiver(post_save, sender=Campaign)
def save_image_on_cloudcare(**kwargs):
    campaign = kwargs['instance']
    try:
        File(campaign.image.cdn_url).store()
    except Exception:
        pass


@receiver(post_delete, sender=Campaign)
def delete_image_on_cloudcare(**kwargs):
    campaign = kwargs['instance']
    try:
        File(campaign.image.cdn_url).store()
    except Exception:
        pass


class CampaignProduct(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='campaign_products')
    target = models.PositiveIntegerField(default=1)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('campaign', 'product')
        ordering = ('product',)

    @property
    def target_value(self):
        return self.target * self.product.price

    def valid_donation_products(self):
        return self.donation_products.objects.filter(
            donation__payment_status="success"
        ).distinct()

    def number_donated(self):
        donation_products = self.valid_donation_products()
        if not donation_products:
            return 0
        return donation_products.aggregate(
            number_donated=Sum("quantity")
        )["number_donated"]


class CampaignProfile(models.Model):
    """this is the profile of the user using the campaign"""
    paid = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='campaign_profile')
