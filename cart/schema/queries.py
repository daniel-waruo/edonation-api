import graphene

from cart.models import Cart, CartProduct
from cart.schema.types import CartType, CartProductType


class Query(graphene.ObjectType):
    cart = graphene.Field(CartType)

    def resolve_cart(self, info, **kwargs):
        request = info.context
        # get and return cart object type
        cart = Cart.objects.get_from_request(request)
        return cart

    cart_products = graphene.List(CartProductType, campaign=graphene.String(required=False))

    def resolve_cart_products(self, info, **kwargs):
        cart_products = CartProduct.objects.filter(cart=self.cart)
        if kwargs.get("campaign"):
            return cart_products.filter(product__campaign__slug=kwargs.get("campaign"))
        return cart_products
