from django.db import models

from elections.models import Election


class Seat(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True,related_name='seats')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
