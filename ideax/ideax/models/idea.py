from django.conf import settings
from django.db import models


class Idea(models.Model):
    title = models.CharField(max_length=200)
    oportunity = models.TextField(max_length=2500, null=True)
    solution = models.TextField(max_length=2500, null=True)
    target = models.TextField(max_length=500, null=True)
    creation_date = models.DateTimeField('data criação')
    author = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='old_author')
    authors = models.ManyToManyField('users.UserProfile', related_name='authors')
    category = models.ForeignKey('Category', models.SET_NULL, null=True)
    discarded = models.BooleanField(default=False)
    score = models.FloatField(default=0)
    category_image = models.CharField(
        max_length=200, default=settings.MEDIA_URL+'category/default.png')
    summary = models.TextField(max_length=140, null=True, blank=False)
    challenge = models.ForeignKey(
        'Challenge', models.SET_NULL, null=True, blank=True)

    def count_popular_vote(self, like_boolean):
        return self.popular_vote_set.filter(like=like_boolean).count()

    def count_dislikes(self):
        return self.count_popular_vote(False)

    def count_likes(self):
        return self.count_popular_vote(True)

    def get_current_phase_history(self):
        return self.phase_history_set.get(current=True)

    def get_current_phase(self):
        return self.phase_history_set.values('current_phase_id').get(current=True)

    def get_absolute_url(self):
        return "/idea/%i/" % self.id

    def get_approval_rate(self):
        sum = self.count_likes() + self.count_dislikes()
        return self.count_likes()/sum*100 if sum > 0 else 0
