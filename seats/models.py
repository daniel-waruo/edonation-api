from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Seat(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
