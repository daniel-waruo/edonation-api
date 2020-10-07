import graphene

from cart.models import Cart, CartProduct
from cart.schema.types import CartType, CartProductType


class Query(graphene.ObjectType):
    cart = graphene.Field(CartType)

    def resolve_cart(self, info):
        request = info.context
        # get and return cart object type
        return Cart.objects.get_from_request(request)

    cart_products = graphene.List(CartProductType)

    def resolve_cart_products(self, info, **kwargs):
        return CartProduct.objects.filter(cart=self.cart)
