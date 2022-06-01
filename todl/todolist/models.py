from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class TodoTags(models.Model):
    tag_name = models.CharField(max_length=60)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # description = models.CharField(max_length=160)


class Todo(models.Model):
    title = models.CharField(max_length=200, blank=True)
    body = models.CharField(max_length=2000, blank=True)
    timestamp_create = models.DateTimeField(auto_now_add=True)
    timestamp_todo = models.DateField()
    timestamp_done = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(TodoTags)


