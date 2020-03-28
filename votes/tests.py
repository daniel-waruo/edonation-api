from django.contrib.auth import get_user_model
from django.test.testcases import TestCase

from candidates.models import Candidate
from elections.models import Election
from seats.models import Seat
from votes.models import Vote, UserVote


class TestVotes(TestCase):

    def setUp(self):
        self.election = Election.objects.create(
            name="Test Election"
        )
        seat = Seat.objects.create(
            election=self.election,
            name="Test Seat"
        )
        self.candidate = Candidate.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@gmail.com",
            seat=seat
        )
        self.user = get_user_model().objects.create(
            username="johndoe",
            email="johndoe@gmail.com",
            password="fake_password"
        )
        self.vote = Vote.objects.create(candidate=self.candidate)

    def test_vote(self):
        # call the add method of objects
        Vote.objects.vote([self.candidate.id], self.election)
        vote = Vote.objects.get(candidate_id=self.candidate.id)
        self.assertIs(vote.number, self.vote.number + 1, "Vote is failing")

    def test_vote_add(self):
        # call the add method of objects
        vote = Vote.objects.add(self.candidate.id)
        self.assertIs(vote.number, self.vote.number + 1, "Vote addition is failing")

    def test_user_vote_add(self):
        user_vote = UserVote.objects.add(self.user, self.election)
        self.assertIsNotNone(user_vote)
