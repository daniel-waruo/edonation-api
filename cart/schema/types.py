import graphene
from graphene_django import DjangoObjectType

from campaigns.schema.types import CampaignType, CampaignProductType
from cart.models import Cart, CartProduct
# This is configured in the CategoryNode's Meta class (as you can see below)
from products.schema.types import ProductType


class CartProductType(DjangoObjectType):
    class Meta:
        model = CartProduct

    campaign_product = graphene.Field(CampaignProductType)

    def resolve_campaign_product(self: CartProduct, info):
        return self.product

    product = graphene.Field(ProductType)

    def resolve_product(self: CartProduct, info):
        return self.product.product

    campaign = graphene.Field(CampaignType)

    def resolve_campaign(self: CartProduct, info):
        return self.product.campaign

    total = graphene.String()

    def resolve_total(self: CartProduct, info):
        return self.quantity * self.product.product.price


class CartType(DjangoObjectType):
    class Meta:
        model = Cart

    products = graphene.List(CartProductType, campaign=graphene.String(required=False))

    def resolve_products(self: Cart, info, **kwargs):
        if kwargs.get("campaign"):
            return self.products.filter(product__campaign__slug=kwargs.get("campaign"))
        return self.products.all()

    number = graphene.Int(campaign=graphene.String(required=False))

    def resolve_number(self: Cart, info, **kwargs):
        products = self.products.all()
        if kwargs.get("campaign"):
            products = self.products.filter(product__campaign__slug=kwargs.get("campaign"))
        return self.number_of_products(queryset=products)

    total = graphene.String(campaign=graphene.String(required=False))

    def resolve_total(self: Cart, info, **kwargs):
        products = self.products.all()
        if kwargs.get("campaign"):
            products = self.products.filter(product__campaign__slug=kwargs.get("campaign"))
        return self.total(queryset=products)
