from django.db import models
from django.utils import timezone


class UseTermManager(models.Manager):
    def get_active(self):
        for term in self.all():
            if term.is_past_due:
                return True
        return False


class Use_Term(models.Model):  # noqa
    creator = models.ForeignKey('users.UserProfile', on_delete=models.PROTECT)
    term = models.TextField(max_length=12500)
    init_date = models.DateTimeField()
    final_date = models.DateTimeField()

    objects = UseTermManager()

    @property
    def is_past_due(self):
        if timezone.now() < self.final_date:
            return True
        return False

    def is_invalid_date(self):
        if self.final_date < self.init_date:
            return True
        return False
