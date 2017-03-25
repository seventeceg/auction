import uuid
import os

from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models

from accounts.settings import AUTH_USER_MODEL

CHOICES = [(i, i) for i in range(1, 6)]


def get_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    name = str(uuid.uuid4()).replace('-', '_')
    filename = '{}.{}'.format(name, ext)
    return os.path.join('images', filename)


class CustomUser(AbstractUser):
    """Structure for a user account database table."""
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=get_image_file_path)
    # Product categories a user is interested in.
    interests = models.CharField(max_length=1000, blank=True)
    # The push notification ID from user' mobile device.
    # This key is used to send push notifications to the user.
    push_key = models.CharField(max_length=1000, blank=True)

    write_only = ('password',)
    USERNAME_FIELD = 'username'


class UserReview(models.Model):
    """Review for an ad poster. Text + Stars."""
    reviewee = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 related_name='reviewee')
    reviewer = models.ForeignKey(AUTH_USER_MODEL, blank=False,
                                 related_name='reviewer')
    review_time = models.DateTimeField(auto_now_add=True)
    review = models.CharField(max_length=2000, blank=True)
    stars = models.IntegerField(blank=False)

    def reviewer_name(self):
        return self.reviewer.username

    def reviewee_name(self):
        return self.reviewee.username


class ProductAd(models.Model):
    """Database structure for a single product ad."""
    # Ad poster ID
    owner = models.ForeignKey(AUTH_USER_MODEL, blank=False, related_name='ad')
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=70, blank=False)
    description = models.CharField(max_length=4000, blank=False)
    category = models.CharField(max_length=100, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    currency = models.CharField(max_length=3, blank=False)
    photo1 = models.ImageField(upload_to=get_image_file_path)
    photo2 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo3 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo4 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo5 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo6 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo7 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo8 = models.ImageField(upload_to=get_image_file_path, blank=True)
    # The estimated number of hours the product will be shipped, after
    # bidding closes.
    delivery_time = models.CharField(max_length=70, blank=False)
    sold = models.BooleanField(default=False)
    sold_to = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return '{} @ {}'.format(self.title, self.price)

    def owner_email(self):
        return CustomUser.objects.get(id=self.owner.id).email


class Bids(models.Model):
    """Database structure for bids on an ad."""
    # ID of the ad this bid is associatd to
    ad = models.ForeignKey(ProductAd, on_delete=models.CASCADE,
                           related_name='bids')
    bid_time = models.DateTimeField(auto_now_add=True)
    # ID of the bidder
    bidder = models.ForeignKey(AUTH_USER_MODEL, blank=False,
                               related_name='bidder')
    # Bid price
    bid = models.DecimalField(max_digits=8, decimal_places=2, blank=False)

    def __str__(self):
        return '{} @ {}'.format(self.bidder, self.bid)

    def bidder_name(self):
        """Return the name of the bidder on an ad."""
        return self.bidder.username


class ProductAdInline(admin.TabularInline):

    model = ProductAd


class AdCategories(models.Model):
    """Ad categories set by the admin. example 'cars', 'estate'."""

    name = models.CharField(max_length=70, blank=False, unique=True)
    photo = models.ImageField(upload_to=get_image_file_path, blank=False)
    id = models.AutoField(primary_key=True)


class Messages(models.Model):
    """Database structure for chat between bidder and owner."""
    ad = models.ForeignKey(ProductAd, on_delete=models.CASCADE,
                           related_name='chat')
    message_time = models.DateTimeField(auto_now_add=True)
    # Incoming or Outgoing
    direction = models.CharField(max_length=8, blank=False)
    # Who sent this message, either its the bidder or the owner
    sender_name = models.CharField(max_length=70, blank=False)
    # The message text
    message = models.CharField(max_length=2000, blank=False)
    # To keep a track of to whom this message thread is associated to
    bidder_name = models.CharField(max_length=70, blank=False)
