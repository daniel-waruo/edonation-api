import graphene
from graphene.utils.str_converters import to_camel_case
from graphene_django import DjangoObjectType
from rest_auth.models import TokenModel

from accounts.models import User
from campaigns.models import CampaignProfile


class Error(graphene.ObjectType):
    """ represent errors
        field - field for which the error is called
        messages - messages in the field
    """
    field = graphene.String()
    messages = graphene.List(graphene.String)


def errors_to_graphene(errors: dict):
    """Changes Serialization Errors to My Graphene Error Type
    Args:
        errors - errors from a serializer
    """
    graphene_errors = []
    # create a list of Error Objects
    for error in errors.keys():
        graphene_errors.append(
            Error(
                field=to_camel_case(error),
                messages=errors[error]
            )
        )
    return graphene_errors


class UserType(DjangoObjectType):
    from campaigns.schema.types import CampaignType
    campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_campaigns(self: User, info, **kwargs):
        campaigns = self.campaigns.filter(deleted=False)
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    def resolve_campaign_profile(self: User, info, **kwargs):
        if hasattr(self, 'campaign_profile'):
            return self.campaign_profile
        return CampaignProfile.objects.create(user=self)

    class Meta:
        model = User
        exclude = ('password',)


class TokenType(DjangoObjectType):
    key = graphene.String(required=True)

    def resolve_key(self, info, **kwargs):
        return self.token_key

    class Meta:
        model = TokenModel
        fields = ["token_key"]
