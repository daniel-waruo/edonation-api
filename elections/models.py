from django.db import models
from django.utils.text import slugify

from accounts.models import User


class ElectionManager(models.Manager):

    def active(self):
        return self.filter(active=True).first()


class Election(models.Model):
    name = models.CharField(max_length=200, unique=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="elections")

    slug = models.SlugField(null=True, editable=False)

    objects = ElectionManager()

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.slug = slugify(self.name.lower())
        super().save(*args, **kwargs)

    class Meta:
        get_latest_by = 'end_date'

    def __str__(self):
        return self.name
# TODO: write validator to make sure only one is active at a time
