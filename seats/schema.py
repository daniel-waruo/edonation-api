import graphene
from graphene_django import DjangoObjectType

from seats.models import Seat


class SeatType(DjangoObjectType):
    class Meta:
        model = Seat


class Query(graphene.ObjectType):
    seat = graphene.Field(SeatType)
