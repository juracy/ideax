import random

from django.db import models


class Category_Image(models.Model):  # noqa
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category/')
    category = models.ForeignKey('Category', models.SET_NULL, null=True)

    @classmethod
    def get_random_image(cls, category):
        id_list = Category_Image.objects.filter(
            category=category).values_list('id', flat=True)
        if id_list:
            return Category_Image.objects.get(id=random.choice(list(id_list)))
        return None
