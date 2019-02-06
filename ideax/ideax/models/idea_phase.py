from django.db import models


class IdeaPhase(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True,  null=True)
    order = models.PositiveSmallIntegerField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Idea Phase"
