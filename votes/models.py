from django.conf import settings
from django.db import models

from candidates.models import Candidate

User = settings.AUTH_USER_MODEL


class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
