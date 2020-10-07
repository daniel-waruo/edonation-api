import graphene

from cart.models import Cart
from cart.schema.types import CartProductType


class CartProductAdd(graphene.Mutation):
    product = graphene.Field(CartProductType)

    class Arguments:
        product_id = graphene.ID(required=False)
        quantity = graphene.Int(required=True)

    def mutate(self, info, product_id, quantity):
        cart = Cart.objects.get_from_request(info.context)
        cart_product = cart.add_product(product_id, quantity)
        return CartProductAdd(
            product=cart_product
        )


class CartProductRemove(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        product_id = graphene.ID(required=False)

    def mutate(self, info, product_id):
        cart = Cart.objects.get_from_request(info.context)
        cart.remove_product(product_id)
        return CartProductRemove(
            success=True
        )


class CartProductUpdate(graphene.Mutation):
    product = graphene.Field(CartProductType)

    class Arguments:
        product_id = graphene.ID(required=False)
        quantity = graphene.Int(required=True)

    def mutate(self, info, product_id, quantity):
        cart = Cart.objects.get_from_request(info.context)
        cart_product = cart.update_product_number(product_id, quantity)
        return CartProductAdd(
            product=cart_product
        )


class Mutation(graphene.ObjectType):
    cart_product_add = CartProductAdd.Field()
    cart_product_remove = CartProductRemove.Field()
    cart_product_update = CartProductUpdate.Field()
