import graphene

from accounts.schema.types import Error, errors_to_graphene
from campaigns.serializers import CampaignSerializer
from .types import CampaignType


class CreateCampaign(graphene.Mutation):
    campaign = graphene.Field(CampaignType)
    errors = graphene.List(Error)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        image = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if not request.user.is_authenticated:
            return None
        kwargs["owner"] = request.user.id
        kwargs["name"] = kwargs["name"].lower()
        serializer = CampaignSerializer(data=kwargs)
        if serializer.is_valid():
            return CreateCampaign(
                campaign=serializer.save()
            )
        return CreateCampaign(
            errors=errors_to_graphene(serializer.errors)
        )


class EditCampaign(graphene.Mutation):
    campaign = graphene.Field(CampaignType)
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()
        image = graphene.String()

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        user = request.user
        # check if user is authenticated
        if not user.is_authenticated:
            return None
        if not user.campaigns.filter(id=kwargs["id"]).exists():
            return EditCampaign(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid Campaign Id"]
                    )
                ]
            )
        if kwargs.get("name"):
            kwargs["name"] = kwargs["name"].lower()
        kwargs["owner"] = user.id
        serializer = CampaignSerializer(
            data=kwargs,
            instance=user.campaigns.get(id=kwargs["id"])
        )
        if serializer.is_valid():
            return EditCampaign(
                campaign=serializer.save()
            )
        return EditCampaign(
            errors=errors_to_graphene(serializer.errors)
        )


class Mutation(graphene.ObjectType):
    create_campaign = CreateCampaign.Field()
    edit_campaign = EditCampaign.Field()
