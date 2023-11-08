from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction_Listings", blank=True, related_name="users")

class Bids(models.Model):
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", blank=True)

class Categories(models.Model):
    cat = models.CharField(max_length=64)

class Auction_Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    biding = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="items")
    is_open = models.BooleanField(default = True)
    image_link = models.URLField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="lists", blank = True, null = True)


class Commenst(models.Model):
    comment = models.CharField(max_length = 512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    item = models.ForeignKey(Auction_Listings, on_delete=models.CASCADE, related_name="comments", null = True)
    likes = models.IntegerField(default=0)
    likedBy = models.ManyToManyField(User, related_name="liked_comments", null=True)
    