from django.db import models
from django.template.defaultfilters import slugify

from elections.models import Election


class Seat(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, related_name='seats')
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, editable=False)

    priority = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.slug = slugify(self.name)
        super(Seat, self).save(*args, **kwargs)

    class Meta:
        unique_together = [
            ['election', 'name'],
            ['election', 'slug']
        ]
        ordering = ['priority']

    def __str__(self):
        return self.name
