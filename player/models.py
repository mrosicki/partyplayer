from django.db import models

# Create your models here.

class Dj(models.Model):
    username = models.fields.TextField(max_length=200, null=True)

    @classmethod
    def create(cls,username):
        new = cls(username=username)
        return new
        