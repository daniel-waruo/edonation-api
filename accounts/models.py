from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


# Create your models here.


class UserManager(BaseUserManager):
    def create_admin_user(self, first_name, last_name, email, phone, creator):
        assert creator.is_authenticated
        assert creator.is_superuser
        return self.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            created_by=creator,
            is_staff=True
        )

    def create_super_user(self, first_name, last_name, email, phone, creator):
        assert creator.is_authenticated
        assert creator.is_superuser
        return self.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            created_by=creator,
            is_superuser=True
        )


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        null=False,
        error_messages={
            'unique': _("The email is already in use"),
        },
    )
    created_by = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=20, null=True)

    objects = UserManager()


@receiver(pre_save, sender=User)
def generate_anonymous_username(**kwargs):
    user = kwargs['instance']
    if user.username == "":
        from .utils import generate_username
        full_name = "{}{}".format(user.first_name, user.last_name)
        user.username = generate_username(full_name)
