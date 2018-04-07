from django.contrib.auth.models import User
from django.db import models

from util.models import AbstractModel


class AbstractCustomer(AbstractModel):
    image = models.URLField()
    phone_number = models.CharField(max_length=12)

    class Meta:
        abstract = True


class Sitter(AbstractCustomer):
    # keys
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fields
    stays = models.PositiveIntegerField(default=0)
    ratings_score = models.FloatField(default=0)
    sitter_score = models.FloatField(default=0)
    overall_score = models.FloatField(default=0)


class Owner(AbstractCustomer):
    # keys
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fields
    dogs = models.CharField(max_length=200)
