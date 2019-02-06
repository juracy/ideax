from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    idea = models.ForeignKey('Idea', on_delete=models.PROTECT)
    author = models.ForeignKey('users.UserProfile', on_delete=models.PROTECT)
    raw_comment = models.TextField()
    parent = TreeForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.PROTECT
    )
    date = models.DateTimeField()
    comment_phase = models.PositiveSmallIntegerField()
    deleted = models.BooleanField(default=False)
    ip = models.CharField(max_length=20, null=True)

    class MPTTMeta:
        order_insertion_by = ['-date']
