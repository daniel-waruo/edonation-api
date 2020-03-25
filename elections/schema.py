import graphene
from graphene_django import DjangoObjectType

from .models import Election


class ElectionType(DjangoObjectType):
    class Meta:
        model = Election


class Query(graphene.ObjectType):
    election = graphene.Field(ElectionType)

    def resolve_election(self, info):
        return Election.objects.active()
