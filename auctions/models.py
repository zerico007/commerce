from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listings(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, default=" ")
    starting_price = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField(auto_now=True)
    listing_photo = models.ImageField(upload_to ='listingPhoto', blank=True)
    CategoryOption = models.TextChoices('CategoryOption', 'Fashion Toys Electronic Home Office Tools')
    category = models.CharField(blank=True, choices=CategoryOption.choices, max_length=90)
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=None)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}: {self.description} at {self.starting_price}"


class Bids(models.Model):
    bid_listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    bid_price = models.DecimalField(max_digits=6, decimal_places=2)
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", default=None)

    def __str__(self):
        return f"{self.bid_listing} : ${self.bid_price}"

class Comments(models.Model):
    comment = models.TextField(max_length=500)
    comment_listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", default=None)
    def __str__(self):
        return f"{self.comment_listing} : {self.comment}"

class Watchlist(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlist")
    watchlist_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists", default=None)

    def __str__(self):
        return f"{self.listing} for {self.watchlist_user}"