import graphene

from products.models import Product
from .types import (
    ProductType
)


class Query(graphene.ObjectType):
    """ Product Query"""
    product = graphene.Field(
        ProductType,
        id=graphene.ID(),
        slug=graphene.String()
    )

    def resolve_product(self, info, id=None, slug=None):
        # check if there is an id specified
        if id:
            if Product.objects.filter(id=id).exists():
                return Product.objects.get(id=id)
        if slug:
            if Product.objects.filter(slug=slug).exists():
                return Product.objects.get(slug=slug)
        return None

    products = graphene.List(ProductType, query=graphene.String())

    def resolve_products(self, info, **kwargs):
        products = Product.objects.filter(deleted=False)
        if kwargs.get("query"):
            products = products.filter(name__icontains=kwargs.get("query"))
        return products
