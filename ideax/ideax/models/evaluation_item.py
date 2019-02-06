from django.db import models

from .criterion import Criterion


class Evaluation_Item(models.Model):  # noqa
    value = models.IntegerField(default=0)
    criterion = models.ForeignKey(Criterion, on_delete=models.PROTECT)
