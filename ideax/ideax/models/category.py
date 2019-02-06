from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    discarded = models.BooleanField(default=False)

    def get_all_image_header(self):
        return self.category_image_set.all()

    def __str__(self):
        return self.title
