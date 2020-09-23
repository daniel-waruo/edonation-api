import graphene

from accounts.schema import Query as UserQuery, Mutation as UserMutation
from products.schema import Query as ProductsQuery, Mutation as ProductsMutation


class Query(UserQuery, ProductsQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(UserMutation, ProductsMutation, graphene.ObjectType):
    # class will inherit multiple mutation
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
