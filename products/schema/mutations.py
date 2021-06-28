import graphene

from utils import Error, errors_to_graphene
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
        image = graphene.String(required=True)

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


class EditProduct(graphene.Mutation):
    product = graphene.Field(ProductType)
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        price = graphene.Decimal()
        description = graphene.String()
        image = graphene.String()

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if not request.user.is_authenticated:
            return None
        if not Product.objects.filter(id=kwargs["id"]).exists():
            return EditProduct(
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
            return EditProduct(
                product=serializer.save()
            )
        return EditProduct(
            errors=errors_to_graphene(serializer.errors)
        )


class DeleteProduct(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(Error)

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        if not Product.objects.filter(id=kwargs["id"]).exists():
            return DeleteProduct(
                errors=[
                    Error(
                        field="non_field_errors",
                        messages=["Invalid Product ID"]
                    )
                ],
            )
        product = Product.objects.get(id=kwargs["id"])
        product.deleted = True
        product.save()
        return DeleteProduct(success=True)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    edit_product = EditProduct.Field()
    delete_product = DeleteProduct.Field()
