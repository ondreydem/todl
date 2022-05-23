from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=200, blank=True)
    body = models.CharField(max_length=2000, blank=True)
    timestamp_create = models.DateTimeField(auto_now_add=True)
    timestamp_todo = models.DateTimeField(blank=True)
    timestamp_done = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
