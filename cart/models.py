from django.db import models
from django.db.models import Sum, F, FloatField

from campaigns.models import CampaignProduct
from cart.errors import NoProductToDelete
from products.models import Product


class CartManager(models.Manager):
    def get_from_request(self, request):
        cart, is_created = self.get_or_create(
            session_key=request.user_session
        )
        return cart


class Cart(models.Model):
    session_key = models.TextField(unique=True, db_index=True)
    created_on = models.DateTimeField(auto_now=True)
    objects = CartManager()

    class Meta:
        verbose_name = 'Cart'

    def __str__(self):
        return "Cart {}".format(self.pk)

    def update_product_number(self, product_pk, product_quantity=1):
        """ Update quantity in a specific product in the cart
        Arguments:
            product_pk - campaign product pk
            product_quantity - the number the products should be updated to

        Returns:
            cart_product - it returns the updated cart product
        """
        if self.products.filter(product=product_pk).exists():
            cart_product = self.products.get(product=product_pk)
            cart_product.quantity = product_quantity
            cart_product.save()
            return cart_product
        # return remove product to handle no existent cases
        # TODO: in future raise no product error
        return self.remove_product(product_pk=product_pk)

    def add_product(self, product_pk, product_quantity=1):
        """ adds a product to the cart
        Arguments:
            product_pk - campaign product pk
            product_quantity - the number the products should be updated to

        Returns:
            cart_product - it returns the updated cart product
        """
        if self.products.filter(product_id=product_pk).exists():
            return self.update_product_number(product_pk, product_quantity)
        return CartProduct.objects.create(
            quantity=product_quantity,
            product_id=product_pk,
            cart=self
        )

    def remove_product(self, product_pk):
        """ remove the product from the cart
        Arguments:
            product_pk - campaign product pk
        Returns:
            cart_product - it returns the deleted cart instance
        """
        if self.products.filter(product=product_pk).exists():
            cart_product = self.products.get(product=product_pk)
            cart_product.delete()
            return cart_product
        raise NoProductToDelete("The product id {0} cannot be deleted.".format(product_pk))

    def number_of_products(self, queryset=None):
        """get the number of products in the cart"""
        if self.products.all().exists():
            if queryset is not None:
                if not queryset:
                    return 0
                return queryset.aggregate(
                    cart_total=Sum("quantity")
                )["cart_total"]
            return self.products.aggregate(
                cart_total=Sum("quantity")
            )["cart_total"]
        return 0

    def total(self, queryset=None):
        """get the total price value of items in the cart """
        if self.products.all().exists():
            if queryset is not None:
                if not queryset:
                    return 0
                return queryset.aggregate(
                    cart_total=Sum(F("quantity") * F("product__product__price"), output_field=FloatField())
                )["cart_total"]
            total = self.products.aggregate(
                cart_total=Sum(F("quantity") * F("product__product__price"), output_field=FloatField())
            )["cart_total"]
            return total
        return 0


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, db_index=True, related_name="products")
    product = models.ForeignKey(CampaignProduct, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'Cart Product'

    def product_total(self):
        return self.quantity * self.product.product.price

    def __str__(self):
        return self.product.product.name
