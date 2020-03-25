import graphene

from accounts.schema import Query as UserQuery
from candidates.schema import Query as CandidateQuery
from elections.schema import Query as ElectionQuery
from seats.schema import Query as SeatQuery


class Query(UserQuery, ElectionQuery, SeatQuery, CandidateQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(
    query=Query,
)
