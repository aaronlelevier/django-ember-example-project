from django.contrib.auth.models import User
from django.db import models

from review.models import RawReview
from util.models import AbstractModel


class AbstractCustomer(AbstractModel):
    name = models.CharField(max_length=50)
    image = models.URLField()
    phone_number = models.CharField(max_length=12)

    class Meta:
        abstract = True


class SitterManager(models.Manager):

    def populate(self):
        for r in RawReview.objects.all():
            try:
                user = User.objects.get(username=r.sitter_email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=r.sitter_email, email=r.sitter_email)

            try:
                self.get(user=user)
            except Sitter.DoesNotExist:
                self.create(user=user, name=r.sitter)



class Sitter(AbstractCustomer):
    # keys
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fields
    stays = models.PositiveIntegerField(default=0)
    ratings_score = models.FloatField(default=0)
    sitter_score = models.FloatField(default=0)
    overall_score = models.FloatField(default=0)

    objects = SitterManager()


class OwnerManager(models.Manager):
    
    def populate(self):
        for r in RawReview.objects.all():
            try:
                user = User.objects.get(username=r.owner_email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=r.owner_email, email=r.owner_email)

            try:
                self.get(user=user)
            except Owner.DoesNotExist:
                self.create(user=user, name=r.owner, dogs=r.dogs)


class Owner(AbstractCustomer):
    # keys
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fields
    dogs = models.CharField(max_length=200)

    objects = OwnerManager()
