from django.db import models


class Phase_History(models.Model):  # noqa
    current_phase = models.ForeignKey('IdeaPhase', on_delete=models.DO_NOTHING)
    previous_phase = models.PositiveSmallIntegerField()
    date_change = models.DateTimeField('data da mudança')
    idea = models.ForeignKey('Idea', on_delete=models.DO_NOTHING)
    author = models.ForeignKey('users.UserProfile', on_delete=models.DO_NOTHING)
    current = models.BooleanField()
