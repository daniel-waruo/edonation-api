from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

# These are gender choices available

gender_choices = (
    ('m', 'MALE'),
    ('f', 'FEMALE'),
    ('u', 'UNKNOWN'),
)


class User(AbstractUser):
    """
    Custom User Class
    """
    email = models.EmailField(
        unique=True,
        null=False,
        error_messages={
            'unique': _("The email is already in use"),
        },
    )

    def get_email(self):
        # function for getting email address
        return self.email
