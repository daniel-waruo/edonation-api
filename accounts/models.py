from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
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

    def is_voted(self, election):
        return self.votes.filter(
            election=election
        ).exists()


# generate unique username if username is blank
# this fixes google's lack of a username
@receiver(pre_save, sender=User)
def generate_anonymous_username(**kwargs):
    user = kwargs['instance']
    if user.username == "":
        from .utils import generate_username
        full_name = "{}{}".format(user.first_name, user.last_name)
        user.username = generate_username(full_name)
