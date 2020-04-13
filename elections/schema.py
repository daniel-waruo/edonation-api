import graphene
from graphene_django import DjangoObjectType

from .models import Election
from .serializers import ElectionSerializers


class ElectionType(DjangoObjectType):
    total_votes = graphene.Int()

    def resolve_total_votes(self: Election, info):
        return self.votes.count()

    class Meta:
        model = Election


class Query(graphene.ObjectType):
    election = graphene.Field(ElectionType, slug=graphene.String())

    def resolve_election(self, info, slug=None):
        if not slug:
            return Election.objects.active()
        else:
            return Election.objects.filter(slug=slug).first()


class AddElection(graphene.Mutation):
    """
      This mutation allows the addition of an election
      through the election manager
    """
    election = graphene.Field(ElectionType)
    errors = graphene.JSONString()

    """Define the data to be sent to the server"""

    class Arguments:
        name = graphene.String(required=True)
        start_date = graphene.String(required=True)
        end_date = graphene.String(required=True)

    """Save the data sent by the user to the db"""

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if request.user.is_authenticated:
            serializer = ElectionSerializers(data=kwargs)
            if serializer.is_valid(raise_exception=False):
                election = serializer.save(user=request.user)
                return AddElection(election=election)

            return AddElection(errors=serializer.errors)

        # raise an exception if the user is not authenticated
        raise Exception("User must Login to add Election")


class Mutation(graphene.ObjectType):
    add_election = AddElection.Field()
