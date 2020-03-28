from django.contrib.auth import get_user_model
from django.test.testcases import TestCase

from elections.models import Election
from votes.models import UserVote


class TestAccounts(TestCase):

    def setUp(self):
        self.election = Election.objects.create(
            name="Test Election"
        )
        self.user = get_user_model().objects.create(
            username="johndoe",
            email="johndoe@gmail.com",
            password="fake_password"
        )

    def test_user_has_voted(self):
        UserVote.objects.add(self.user, self.election)
        user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(user.is_voted(self.election), "User is Voted has failed")

    def test_user_has_not_voted(self):
        user = get_user_model().objects.get(id=self.user.id)
        self.assertFalse(user.is_voted(self.election), "User is Not Voted has failed")

