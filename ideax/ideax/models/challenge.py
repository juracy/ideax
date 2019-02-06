from django.db import models


class Challenge(models.Model):
    image = models.ImageField(upload_to='challenges/')
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=140, null=True, blank=False)
    requester = models.CharField(max_length=140, null=True, blank=False)
    description = models.TextField(max_length=2500)
    limit_date = models.DateTimeField()
    init_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    author = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    featured = models.BooleanField(default=False)
    category = models.ForeignKey('Category', models.SET_NULL, null=True)
    discarted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
