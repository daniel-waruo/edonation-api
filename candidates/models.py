from django.conf import settings
from django.db import models
from pyuploadcare.dj.models import ImageField

from seats.models import Seat

User = settings.AUTH_USER_MODEL


class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    image = ImageField()

    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="candidates")

    def __str__(self):
        return "{} {} ".format(self.first_name, self.last_name)
