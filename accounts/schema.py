import graphene
from graphene_django import DjangoObjectType

from accounts.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)

    def resolve_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None
