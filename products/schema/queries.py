import graphene

from products.models import Product, Category
from .types import (
    ProductType, CategoryType, FilterProducts
)
from ..utils import filter_products, filter_by_price


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

    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    """Filter Products"""
    filter_products = graphene.Field(
        FilterProducts,
        categorySlugs=graphene.List(graphene.String),
        category_Ids=graphene.List(graphene.String),
        query=graphene.String(),
        min=graphene.String(),
        max=graphene.String()
    )

    def resolve_filter_products(self, info, **kwargs):
        category_slug = kwargs.get("categorySlugs")
        if category_slug:
            category_slug = category_slug[0]

        category = None
        if category_slug:
            if Category.objects.filter(slug=category_slug).exists():
                category = Category.objects.get(slug=category_slug)
        # filter by category query
        all_products = filter_products(kwargs)
        # filter by price
        query_set = filter_by_price(all_products, kwargs)
        return FilterProducts(
            all_products=all_products,
            products=query_set,
            category=category
        )

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
