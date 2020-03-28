import graphene
from graphene_django.types import DjangoObjectType

from candidates.models import Candidate
from candidates.schema import CandidateType
from elections.models import Election
from votes.models import Vote, UserVote


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


class SubmitVote(graphene.Mutation):
    """
      Vote class allows a user to cast his/her vote in the election
    """
    candidates = graphene.List(CandidateType)

    """Define the data to be sent to the server"""

    class Arguments:
        candidate_ids = graphene.List(graphene.String, required=True)

    """Save the data sent by the user to the db"""

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if request.user.is_authenticated:
            # get candidate_ids from mutation arguments
            candidate_ids = kwargs.get("candidate_ids")
            # get the active election
            election = Election.objects.active()
            # check if the user has already voted
            if not request.user.is_voted(election=election):
                # vote
                Vote.objects.vote(candidate_ids=candidate_ids, election=election)
                # make user as voted
                UserVote.objects.add(request.user, election)
                return Candidate.objects.filter(id__in=candidate_ids, seat__election=election)
            # else raise an exception
            else:
                raise Exception("You have already voted in this election")
        # if user is not authenticated raise an exception
        raise Exception("Login to vote")


class Mutation(graphene.ObjectType):
    submit_vote = SubmitVote.Field()


class Query(graphene.ObjectType):
    vote = graphene.Field(
        Vote,
        candidate_id=graphene.String(required=True)
    )

    def resolve_vote(self, info, candidate_id):
        return Vote.objects.get(id=candidate_id)
