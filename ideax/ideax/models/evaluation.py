from django.db import models


class Evaluation(models.Model):
    valuator = models.ForeignKey('users.UserProfile', on_delete=models.PROTECT)
    idea = models.ForeignKey('Idea', on_delete=models.PROTECT)
    dimension = models.ForeignKey('Dimension', on_delete=models.PROTECT)
    category_dimension = models.ForeignKey(
        'Category_Dimension', on_delete=models.PROTECT)
    evaluation_date = models.DateTimeField()
    dimension_value = models.IntegerField()
    note = models.TextField(null=True)
