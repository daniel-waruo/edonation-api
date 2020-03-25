import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField

from .models import Candidate


@convert_django_field.register(ImageField)
def convert_field(field, registry=None):
    return graphene.String()


class CandidateType(DjangoObjectType):
    class Meta:
        model = Candidate


class Query(graphene.ObjectType):
    candidate = graphene.Field(CandidateType)
