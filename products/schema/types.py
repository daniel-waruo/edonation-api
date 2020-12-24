import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField

from products.models import Product, Category, ProductImage

def filter_products(qs,query=None,number=None,from_item=None,**kwargs):
    """ This funtion is the one we will use to search and paginate products
    Arguments:
        qs - the campaigns query set to be filtered
        query -  the query if available
        number - the number of items
        last_item - the position of the last item on the list
    """
    if query:
        qs = qs.filter(name__icontains=query)
    # if both parameters are provided
    if not (number is None or from_item is None):
        # get the number items from the last item to the number of items
        qs = qs[from_item:from_item+number]
    return qs

@convert_django_field.register(ImageField)
def convert_field(field, registry=None):
    return graphene.String()


class CategoryType(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self: Category, info):
        return self.name.title()

    class Meta:
        model = Category


class ProductType(DjangoObjectType):
    class Meta:
        model = Product

    name = graphene.String()

    def resolve_name(self: Product, info):
        return self.name.title()

    number_donated = graphene.Int()

    def resolve_number_donated(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return 0
        return self.number_donated


class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        fields = ("id", "url", "product")
