from django.db import models


class Popular_Vote(models.Model):  # noqa
    like = models.BooleanField()
    voter = models.ForeignKey('users.UserProfile', on_delete=models.PROTECT)
    voting_date = models.DateTimeField()
    idea = models.ForeignKey('Idea', on_delete=models.PROTECT)
