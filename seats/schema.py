import graphene
from graphene_django import DjangoObjectType

from seats.models import Seat
from seats.serializers import AddSeatSerializer


class SeatType(DjangoObjectType):
    class Meta:
        model = Seat


class Query(graphene.ObjectType):
    seat = graphene.Field(
        SeatType,
        slug=graphene.String(required=True),
        election_slug=graphene.String(required=True)
    )

    def resolve_seat(self, info, slug, election_slug):
        return Seat.objects.filter(
            election__slug=election_slug,
            slug=slug
        ).first()


class AddSeat(graphene.Mutation):
    """
      This mutation allows the addition of a seat
      through the election manager
    """
    seat = graphene.Field(SeatType)
    errors = graphene.JSONString()

    """Define the data to be sent to the server"""

    class Arguments:
        name = graphene.String(required=True)
        election_slug = graphene.String(required=True)

    """Save the data sent by the user to the db"""

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if request.user.is_authenticated:
            # add election to data base
            serializer = AddSeatSerializer(data=kwargs)
            if serializer.is_valid():
                # return an election
                return AddSeat(seat=serializer.save())
            return AddSeat(errors=serializer.errors)
        # raise an exception if the user is not authenticated
        raise Exception("User must Login to add Election")


class Mutation(graphene.ObjectType):
    add_seat = AddSeat.Field()
