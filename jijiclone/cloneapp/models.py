from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser

import uuid


class Seller(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=100, null=False)
    lastname = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255)
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=False)
    image_url = models.CharField(max_length=255, null=False)
    action = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    buyer_email = models.CharField(max_length=100, null=False)
    buyer_name = models.CharField(max_length=255, null=False)
    buyer_location = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
