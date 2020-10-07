import graphene
from graphene_django import DjangoObjectType

from campaigns.schema.types import CampaignType
from cart.models import Cart, CartProduct
# This is configured in the CategoryNode's Meta class (as you can see below)
from products.schema.types import ProductType


class CartType(DjangoObjectType):
    class Meta:
        model = Cart

    number = graphene.Int()

    def resolve_number(self: Cart, info):
        return self.number_of_products()

    total = graphene.String()

    def resolve_total(self: Cart, info):
        return self.total


class CartProductType(DjangoObjectType):
    class Meta:
        model = CartProduct

    product = graphene.Field(ProductType)

    def resolve_product(self: CartProduct, info):
        return self.product.product

    campaign = graphene.Field(CampaignType)

    def resolve_campaign(self: CartProduct, info):
        return self.product.campaign

    total = graphene.String()

    def resolve_total(self: CartProduct, info):
        return self.quantity * self.product.product.price
