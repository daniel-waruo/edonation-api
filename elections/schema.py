import graphene
from graphene_django import DjangoObjectType

from .models import Election
from .serializers import ElectionSerializer, DeleteElectionSerializer


class ElectionType(DjangoObjectType):
    total_votes = graphene.Int()

    def resolve_total_votes(self: Election, info):
        return self.votes.count()

    created_by = graphene.String()

    def resolve_created_by(self: Election, info):
        full_name = "{} {}".format(self.user.first_name, self.user.last_name)
        return full_name if full_name.strip() != "" else self.user.username

    class Meta:
        model = Election
        exclude = ['user']


class Query(graphene.ObjectType):
    election = graphene.Field(ElectionType, slug=graphene.String())

    def resolve_election(self, info, slug=None):
        if not slug:
            return Election.objects.active()
        else:
            return Election.objects.filter(slug=slug).first()

    elections = graphene.List(ElectionType, index=graphene.Int(), limit=graphene.Int())

    def resolve_elections(self, info, index=1, limit=100):
        # subtract 1 from the index to make it more human friendly
        index -= 1
        return Election.objects.all()[index:index + limit]


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

    """Save the election in the db"""

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if request.user.is_authenticated:
            serializer = ElectionSerializer(data=kwargs, context=request)
            if serializer.is_valid(raise_exception=False):
                election = serializer.save()
                return AddElection(election=election)

            return AddElection(errors=serializer.errors)

        # raise an exception if the user is not authenticated
        raise Exception("User must Login to add Election")


class EditElectionMutation(graphene.Mutation):
    """
      This mutation allows the editing of an election
      through the election manager
    """
    election = graphene.Field(ElectionType)
    errors = graphene.JSONString()

    """Define the data to be sent to the server"""

    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        start_date = graphene.String(required=True)
        end_date = graphene.String(required=True)

    """Save the data sent by the user to the db"""

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if request.user.is_authenticated:
            try:
                serializer = ElectionSerializer(
                    instance=Election.objects.get(id=kwargs["id"]),
                    data=kwargs,
                    context=request
                )
            except Election.DoesNotExist:
                raise Exception("Invalid Election ID")

            if serializer.is_valid(raise_exception=False):
                election = serializer.save()
                return EditElectionMutation(election=election)

            return EditElectionMutation(errors=serializer.errors)

        # raise an exception if the user is not authenticated
        raise Exception("User must Login to edit an Election")


class DeleteElectionMutation(graphene.Mutation):
    """
      This mutation allows the editing of an election
      through the election manager
    """
    success = graphene.Boolean()
    errors = graphene.JSONString()

    """Define the data to be sent to the server"""

    class Arguments:
        id = graphene.String(required=True)
        password = graphene.String(required=True)

    """delete the user in the database"""

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if request.user.is_authenticated:
            try:
                election = Election.objects.get(id=kwargs["id"])
                serializer = DeleteElectionSerializer(
                    context=request,
                    instance=election,
                    data=kwargs
                )
                # check if serializer is valid
                if serializer.is_valid():
                    serializer.save()
                    return DeleteElectionMutation(success=True)
                # return user made errors
                return DeleteElectionMutation(errors=serializer.errors)
            except Election.DoesNotExist:
                raise Exception("Invalid Election ID")

        # raise an exception if the user is not authenticated
        raise Exception("User must Login to delete an Election")


class Mutation(graphene.ObjectType):
    add_election = AddElection.Field()
    edit_election = EditElectionMutation.Field()
    delete_election = DeleteElectionMutation.Field()
