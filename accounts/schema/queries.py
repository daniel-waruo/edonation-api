import graphene

from accounts.models import User
from accounts.schema.types import UserType


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)

    def resolve_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None

    users = graphene.List(UserType,query=graphene.String())

    def resolve_users(self, info, **kwargs):
        request = info.context
        user = request.user
        if not user.is_authenticated or not user.is_staff:
            return
        return User.objects.all()
