import graphene
from graphene_django import DjangoObjectType

from accounts.models import User
from elections.models import Election


class UserType(DjangoObjectType):
    voted = graphene.Boolean()

    def resolve_voted(self: User, info):
        election = Election.objects.active()
        return self.is_voted(election)

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
