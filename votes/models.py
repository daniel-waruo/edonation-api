from django.conf import settings
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from candidates.models import Candidate
from elections.models import Election

User = settings.AUTH_USER_MODEL


class VoteManager(models.Manager):

    def vote(self, candidate_ids, election):
        # get vote objects whose candidate ids ate in the list candidate ids
        votes = self.select_for_update().filter(candidate_id__in=candidate_ids, candidate__seat__election=election)
        # lock the list of vote objects used for this process
        with transaction.atomic():
            for vote in votes:
                for candidate_id in candidate_ids:
                    if vote.candidate.id == int(candidate_id):
                        self.add(candidate_id)

    def add(self, candidate_id):
        if Candidate.objects.filter(id=candidate_id).exists():
            vote, _ = self.get_or_create(candidate_id=candidate_id)
            vote.number += 1
            vote.save()
            return vote
        else:
            raise Exception("Candidate ID is not valid")


class Vote(models.Model):
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, db_index=True, related_name="votes")
    number = models.PositiveIntegerField(default=0)

    objects = VoteManager()


class UserVoteManager(models.Manager):
    def add(self, user, election):
        if user.is_authenticated:
            return self.create(user=user, election=election)
        raise Exception("Only authenticated Users can Vote")


# create a vote instance after the candidate has been created
@receiver(post_save, sender=Candidate)
def create_vote(**kwargs):
    if kwargs['created'] or not Vote.objects.filter(candidate=kwargs['instance']).exists():
        Vote.objects.create(candidate=kwargs['instance'])


class UserVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    election = models.ForeignKey(Election, models.CASCADE, related_name='users')

    objects = UserVoteManager()

    class Meta:
        unique_together = ['user', 'election']
