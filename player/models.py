from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Song(models.Model):
    dj = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=1000)
    wasPlayed = models.BooleanField(default=False)
        