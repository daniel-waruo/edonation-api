import graphene

from accounts.schema.types import Error, errors_to_graphene
from products.serializers import ProductSerializer
from .types import ProductType
from ..models import Product


class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)
    errors = graphene.List(Error)

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        description = graphene.String(required=True)
        images = graphene.List(graphene.String)

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if not request.user.is_authenticated:
            return None
        serializer = ProductSerializer(data=kwargs)
        if serializer.is_valid():
            return CreateProduct(
                product=serializer.save()
            )
        return CreateProduct(
            errors=errors_to_graphene(serializer.errors)
        )


class UpdateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        price = graphene.Decimal()
        description = graphene.String()

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if not request.user.is_authenticated:
            return None
        if not Product.objects.filter(id=kwargs["id"]).exists():
            return UpdateProduct(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid Product Id"]
                    )
                ]
            )
        serializer = ProductSerializer(
            data=kwargs,
            instance=Product.objects.get(id=kwargs["id"])
        )
        if serializer.is_valid():
            return UpdateProduct(
                product=serializer.save()
            )
        return UpdateProduct(
            errors=errors_to_graphene(serializer.errors)
        )


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
