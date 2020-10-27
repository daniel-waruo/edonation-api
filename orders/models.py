from django.db import models

from campaigns.models import CampaignProduct


class Order(models.Model):
    order_time = models.DateTimeField(auto_now_add=True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(CampaignProduct, on_delete=models.CASCADE, related_name="order_products")
    is_delivered = models.BooleanField(default=False)
