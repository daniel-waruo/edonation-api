import graphene
from django.contrib.auth import get_user_model

User = get_user_model()


class Query(graphene.ObjectType):
    pass
