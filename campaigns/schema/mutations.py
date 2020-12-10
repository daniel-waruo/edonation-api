import graphene

from accounts.schema.types import Error, errors_to_graphene
from campaigns.serializers import CampaignSerializer, CampaignProductSerializer, ProductRequestSerializer
from .types import CampaignType, CampaignProductType, ProductRequestType
from ..models import Campaign


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


class AddCampaignProductMutation(graphene.Mutation):
    """add a product to the campaign """

    class Arguments:
        campaign_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)
        target = graphene.Int(required=True)

    product = graphene.Field(CampaignProductType)
    errors = graphene.List(Error)

    def mutate(self, info, **kwargs):

        user = info.context.user
        # check if user is authenticated
        if not user.is_authenticated:
            return None
        serializer = CampaignProductSerializer(
            data={
                "campaign": kwargs["campaign_id"],
                "product": kwargs["product_id"],
                "target": kwargs["target"]
            }
        )
        if serializer.is_valid():
            return AddCampaignProductMutation(
                product=serializer.save()
            )
        return AddCampaignProductMutation(
            errors=errors_to_graphene(serializer.errors)
        )


class ApproveCampaignMutation(graphene.Mutation):
    campaign = graphene.Field(CampaignType)
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        if not Campaign.objects.filter(id=kwargs["id"]).exists():
            return ApproveCampaignMutation(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid campaign ID"]
                    )
                ]
            )
        campaign = Campaign.objects.get(id=kwargs["id"])
        campaign.is_approved = True
        campaign.save()
        return ApproveCampaignMutation(
            campaign=campaign
        )


class DisapproveCampaignMutation(graphene.Mutation):
    campaign = graphene.Field(CampaignType)
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        if not Campaign.objects.filter(id=kwargs["id"]).exists():
            return DisapproveCampaignMutation(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid campaign ID"]
                    )
                ]
            )
        campaign = Campaign.objects.get(id=kwargs["id"])
        campaign.is_approved = False
        campaign.save()
        return DisapproveCampaignMutation(
            campaign=campaign
        )


class SetFeatured(graphene.Mutation):
    campaign = graphene.Field(CampaignType)
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.Int(required=True)
        is_featured = graphene.Boolean(required=True)

    def mutate(self, info, **kwargs):
        if not Campaign.objects.filter(id=kwargs["id"]).exists():
            return ApproveCampaignMutation(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid campaign ID"]
                    )
                ]
            )
        campaign = Campaign.objects.get(id=kwargs["id"])
        campaign.is_featured = kwargs["is_featured"]
        campaign.save()
        return ApproveCampaignMutation(
            campaign=campaign
        )

class DeleteCampaign(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        if not Campaign.objects.filter(id=kwargs["id"]).exists():
            return DeleteCampaign(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid Campaign ID"]
                    )
                ],
            )
        campaign = Campaign.objects.get(id=kwargs["id"])
        campaign.deleted = True
        campaign.save()
        campaign.complete()
        return DeleteCampaign(success=True)


class DeleteCampaignProduct(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(Error)

    class Arguments:
        campaign_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        campaign_id = kwargs["campaign_id"]
        product_id = kwargs["product_id"]
        if not Campaign.objects.filter(id=campaign_id).exists():
            return DeleteCampaignProduct(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid Campaign ID"]
                    )
                ],
            )
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_product = campaign.products.get(product_id=product_id)
        campaign_product.deleted = True
        campaign_product.save()
        return DeleteCampaignProduct(success=True)


class UpdateCampaignProduct(graphene.Mutation):
    product = graphene.Field(CampaignProductType)
    errors = graphene.List(Error)

    class Arguments:
        campaign_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)
        target = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        campaign_id = kwargs["campaign_id"]
        product_id = kwargs["product_id"]
        target = kwargs["target"]
        if not Campaign.objects.filter(id=campaign_id).exists():
            return UpdateCampaignProduct(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid Campaign ID"]
                    )
                ],
            )
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_product = campaign.products.get(product_id=product_id)
        campaign_product.target = target
        campaign_product.save()
        return UpdateCampaignProduct(product=campaign_product)


class RestoreCampaignProduct(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(Error)

    class Arguments:
        campaign_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        campaign_id = kwargs["campaign_id"]
        product_id = kwargs["product_id"]
        if not Campaign.objects.filter(id=campaign_id).exists():
            return RestoreCampaignProduct(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid Campaign ID"]
                    )
                ],
            )
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_product = campaign.products.get(product_id=product_id)
        campaign_product.deleted = False
        campaign_product.save()
        return RestoreCampaignProduct(success=True)


class CloseCampaign(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        if not Campaign.objects.filter(id=kwargs["id"]).exists():
            return CloseCampaign(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid Campaign ID"]
                    )
                ],
            )
        campaign = Campaign.objects.get(id=kwargs["id"])
        campaign.complete()
        return CloseCampaign(success=True)


class CreateProductRequest(graphene.Mutation):
    product_request = graphene.Field(ProductRequestType)
    errors = graphene.List(Error)

    class Arguments:
        campaign_id = graphene.Int(required=True)
        request = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if not request.user.is_authenticated:
            return None
        kwargs["campaign"] = kwargs["campaign_id"]
        serializer = ProductRequestSerializer(data=kwargs)
        if serializer.is_valid():
            return CreateProductRequest(
                product_request=serializer.save()
            )
        return CreateProductRequest(
            errors=errors_to_graphene(serializer.errors)
        )


class Mutation(graphene.ObjectType):
    create_campaign = CreateCampaign.Field()
    edit_campaign = EditCampaign.Field()
    add_campaign_product = AddCampaignProductMutation.Field()

    approve_campaign = ApproveCampaignMutation.Field()
    disapprove_campaign = DisapproveCampaignMutation.Field()
    set_featured = SetFeatured.Field()
    delete_campaign = DeleteCampaign.Field()
    close_campaign = CloseCampaign.Field()

    delete_campaign_product = DeleteCampaignProduct.Field()
    update_campaign_product = UpdateCampaignProduct.Field()
    restore_campaign_product = RestoreCampaignProduct.Field()

    create_product_request = CreateProductRequest.Field()
