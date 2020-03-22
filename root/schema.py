import graphene

from accounts.schema import (
    Query as UserQuery
)


class Query(UserQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(
    query=Query,
)
