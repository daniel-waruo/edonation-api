import graphene
from django.db.models import Count
from graphene.utils.str_converters import to_camel_case
from graphene_django import DjangoObjectType
from rest_auth.models import TokenModel

from accounts.models import User
from campaigns.models import CampaignProfile
from donations.models import Donation


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
    from campaigns.schema.types import CampaignType, CampaignProfileType
    from donations.schema.types import DonationType
    from campaigns.schema.types import DonationDateType
    campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_campaigns(self: User, info, **kwargs):
        campaigns = self.campaigns.filter(deleted=False, is_active=True)
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    campaign_number = graphene.Int()

    def resolve_campaign_number(self: User, info, **kwargs):
        campaigns = self.campaigns.filter(deleted=False, is_active=True)
        return campaigns.count()

    complete_campaigns = graphene.List(CampaignType, query=graphene.String())

    def resolve_complete_campaigns(self: User, info, **kwargs):
        campaigns = self.campaigns.filter(is_active=False, delivery__isnull=False)
        if kwargs.get("query"):
            campaigns = campaigns.filter(name__icontains=kwargs.get("query"))
        return campaigns

    complete_campaign_number = graphene.Int()

    def resolve_complete_campaign_number(self: User, info, **kwargs):
        campaigns = self.campaigns.filter(is_active=False, delivery__isnull=False)
        return campaigns.count()

    donations = graphene.List(DonationType)

    def resolve_donations(self, info, **kwargs):
        return Donation.objects.filter(
            products__product__campaign__in=self.campaigns.all(),
            payment_status="success"
        )

    donation_number = graphene.Int()

    def resolve_donation_number(self, info, **kwargs):
        return Donation.objects.filter(
            products__product__campaign__in=self.campaigns.all(),
            payment_status="success"
        ).count()

    donations_by_date = graphene.List(DonationDateType)

    def resolve_donations_by_date(self, info, **kwargs):
        from campaigns.schema.types import DonationDateType

        donations = Donation.objects.filter(
            products__product__campaign__in=self.campaigns.all(),
            payment_status="success"
        ).extra({'date': "date(created_on)"}).values('date').annotate(number=Count('id'))
        return list(map(lambda x: DonationDateType(date=x["date"], number=x["number"]), donations))

    campaign_profile = graphene.Field(CampaignProfileType)

    def resolve_campaign_profile(self: User, info, **kwargs):
        if CampaignProfile.objects.filter(user=self).exists():
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
