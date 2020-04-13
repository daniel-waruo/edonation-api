import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField

from elections.models import Election
from .models import Candidate
from .serializers import AddCandidateSerializer


@convert_django_field.register(ImageField)
def convert_field(field, registry=None):
    return graphene.String()


class CandidateType(DjangoObjectType):
    class Meta:
        model = Candidate


class Query(graphene.ObjectType):
    candidates = graphene.List(
        CandidateType,
        slug=graphene.String(required=True)
    )

    def resolve_candidates(self, info, **kwargs):
        # get the active election
        election = Election.objects.active()
        # get slug from query
        slug = kwargs.get("slug")
        # get the candidates linked to the slug and election
        candidates = Candidate.objects.filter(
            seat__slug=slug,
            seat__election=election
        )
        # return candidates
        return candidates

    candidate = graphene.Field(
        CandidateType,
        id=graphene.String(required=True)
    )

    def resolve_candidate(self, info, **kwargs):
        candidate_id = kwargs.get("id")
        try:
            return Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return None


class AddCandidate(graphene.Mutation):
    """
      This mutation allows the addition of a candidate
      through the election manager
    """
    candidate = graphene.Field(CandidateType)
    errors = graphene.JSONString()

    """Define the data to be sent to the server"""

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        image = graphene.String(required=True)
        seat_id = graphene.String(required=True)

    """Save the data sent by the user to the db"""

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if request.user.is_authenticated:
            # add election to data base
            serializer = AddCandidateSerializer(data=kwargs, context=request)
            if serializer.is_valid():
                # return an election
                return AddCandidate(candidate=serializer.save())
            return AddCandidate(errors=serializer.errors)
        # raise an exception if the user is not authenticated
        raise Exception("User must Login to add Candidate")


class Mutation(graphene.ObjectType):
    add_candidate = AddCandidate.Field()
