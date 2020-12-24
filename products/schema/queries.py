import graphene

from products.models import Product, Category
from .types import (
    ProductType,
    CategoryType,
    filter_products
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

    products = graphene.List(
        ProductType,
        query=graphene.String(),
        number=graphene.Int(),
        from_item=graphene.Int()
    )

    def resolve_products(self, info, **kwargs):
        products = Product.objects.filter(deleted=False)
        return filter_products(products,**kwargs)

    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    all_featured_products = graphene.List(ProductType)

    def resolve_all_featured_products(self, info, **kwargs):
        products = Product.objects.filter(deleted=False)
        products = products.filter(featured=True)
        return products

    donated_products = graphene.List(ProductType)

    def resolve_donated_products(self, info, **kwargs):
        """
        Get all the products donated to a certain user
        :param info:
        :param kwargs:
        :return:
        """
        user = info.context.user
        if not user.is_authenticated:
            return None

        donated_products = Product.objects.filter(
            deleted=False,
            campaign_products__campaign__owner=user,
            campaign_products__donation_products__donation__payment_status="success",
        ).distinct()
        return donated_products
