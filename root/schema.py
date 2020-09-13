import graphene

from accounts.schema import Query as UserQuery, Mutation as UserMutation


class Query(UserQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(UserMutation, graphene.ObjectType):
    # class will inherit multiple mutation
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
