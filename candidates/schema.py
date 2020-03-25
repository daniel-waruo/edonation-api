import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField

from elections.models import Election
from .models import Candidate


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
