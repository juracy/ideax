from django.db import models

from .evaluation_item import Evaluation_Item


class Vote(models.Model):
    evaluation_item = models.ForeignKey(
        Evaluation_Item, on_delete=models.PROTECT)
    value = models.IntegerField()
    voter = models.ForeignKey('users.UserProfile', on_delete=models.PROTECT)
    idea = models.ForeignKey('Idea', on_delete=models.PROTECT)
    voting_date = models.DateTimeField('data da votação')
