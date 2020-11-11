import graphene

from accounts.schema import Query as UserQuery, Mutation as UserMutation
from campaigns.schema import Query as CampaignsQuery, Mutation as CampaignMutation
from cart.schema import Query as CartQuery, Mutation as CartMutation
from donations.schema import Query as DonationsQuery
from payments.schema import Query as PaymentQuery, Mutation as PaymentMutation
from products.schema import Query as ProductsQuery, Mutation as ProductsMutation


class Query(UserQuery, ProductsQuery, CampaignsQuery, CartQuery, PaymentQuery, DonationsQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(UserMutation, ProductsMutation, CampaignMutation, CartMutation, PaymentMutation, graphene.ObjectType):
    # class will inherit multiple mutation
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
