from django.db import models


class ElectionManager(models.Manager):

    def active(self):
        return self.filter(active=True).first()


class Election(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    active = models.BooleanField(null=True)

    objects = ElectionManager()

    class Meta:
        get_latest_by = 'end_date'

    def __str__(self):
        return self.name
# TODO: write validator to make sure only one is active at a time
