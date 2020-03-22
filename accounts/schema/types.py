from graphene_django import DjangoObjectType

from ..models import User


# This is configured in the CategoryNode's Meta class (as you can see below)
class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)
