from django.db import models


class Dimension(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    weight = models.IntegerField()
    init_date = models.DateTimeField()
    final_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
