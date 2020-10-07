import django_filters
import graphene
from django.db.models import Min, Max
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.filter import DjangoFilterConnectionField
from pyuploadcare.dj.models import ImageField

from cart.models import Cart
from products.models import Product, Category, ProductImage


@convert_django_field.register(ImageField)
def convert_field(field, registry=None):
    return graphene.String()


class CategoryType(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self: Category, info):
        return self.name.title()

    class Meta:
        model = Category


class ProductNode(DjangoObjectType):
    pk = graphene.String()

    def resolve_pk(self, info):
        return self.pk

    class Meta:
        model = Product
        # Allow for some more advanced filtering here
        filter_fields = [
            'id',
            'slug',
            'category'
        ]
        interfaces = (relay.Node,)


class ProductType(DjangoObjectType):
    class Meta:
        model = Product

    name = graphene.String()

    def resolve_name(self: Product, info):
        return self.name.title()

    in_cart = graphene.Boolean()

    def resolve_in_cart(self: Product, info):
        cart = Cart.objects.get_from_request(info.context)
        return cart.products.filter(product_id=self.id).exists()


class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        fields = ("id", "url", "product")


class FilterPriceType(graphene.ObjectType):
    min = graphene.Int()
    max = graphene.Int()


class ProductFilter(django_filters.FilterSet):
    # Do case-insensitive lookups on 'name'
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), to_field_name='id')

    class Meta:
        model = Product
        fields = ['id', 'slug']


class FilterProducts(graphene.ObjectType):
    products = DjangoFilterConnectionField(
        ProductNode,
        filterset_class=ProductFilter,
    )

    all_products = DjangoFilterConnectionField(
        ProductNode,
        filterset_class=ProductFilter,
    )

    filter_price = graphene.Field(FilterPriceType)

    category = graphene.Field(CategoryType)

    def resolve_filter_price(self, info, **kwargs):
        products = self.all_products
        price_dict = products.aggregate(Min('price'), Max('price'))
        return FilterPriceType(
            min=price_dict['price__min'],
            max=price_dict['price__max']
        )
