from django.contrib.auth import get_user_model
from django.db import models
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

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


@receiver(post_save, sender=Campaign)
def save_image_on_cloudcare(**kwargs):
    campaign = kwargs['instance']
    File(campaign.image.cdn_url).store()


@receiver(post_delete, sender=Campaign)
def delete_image_on_cloudcare(**kwargs):
    campaign = kwargs['instance']
    File(campaign.image.cdn_url).delete()


class CampaignProduct(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
