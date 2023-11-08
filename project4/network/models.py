from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    follow = models.ManyToManyField('self', symmetrical = False ,related_name="followers")

class Post(models.Model):
    content = models.CharField(max_length = 256)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="Posts")
    time = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name = "liked_posts", blank=True)


