from django.db import models


class Category_Dimension(models.Model):  # noqa
    description = models.CharField(max_length=200)
    value = models.IntegerField()
    dimension = models.ForeignKey('Dimension', on_delete=models.PROTECT)

    def __str__(self):
        return self.description
