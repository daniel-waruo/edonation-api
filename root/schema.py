import graphene

from accounts.schema import Query as UserQuery
from candidates.schema import Query as CandidateQuery
from elections.schema import Query as ElectionQuery
from seats.schema import Query as SeatQuery
from votes.schema import Mutation as VotesMutation


class Query(UserQuery, ElectionQuery, SeatQuery, CandidateQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(VotesMutation, graphene.ObjectType):
    # class will inherit multiple mutation
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
