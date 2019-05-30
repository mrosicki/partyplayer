from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class dj(models.Model):
    username = models.fields.TextField(max_length=200, null=True)

    @classmethod
    def create(cls,username):
        new = cls(username=username)
        return new


