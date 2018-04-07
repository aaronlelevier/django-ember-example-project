import os
import csv
from django.conf import settings
from django.db import models

from customer.models import Sitter, Owner
from util.models import AbstractModel


class RawReviewManager(models.Manager):

    def populate(self):
        count = self.count()
        if count > 0:
            raise AssertionError(
                'RawReview is alredy populated with {} records'.format(count))

        with open(os.path.join(settings.DATA_DIR, 'reviews.csv')) as csvfile:
            reader = csv.DictReader(csvfile)
            self.bulk_create(
                [self.model(**r) for r in reader])


class RawReview(models.Model):
    """
    Table from CSV import of 'reviews.csv'. To be kept as a
    raw table and not queried in production
    """
    rating = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    text = models.TextField()
    dogs = models.CharField(max_length=200)
    # owner
    owner = models.CharField(max_length=100)
    owner_image = models.URLField()
    owner_phone_number = models.CharField(max_length=12)
    owner_email = models.EmailField()
    # sitter
    sitter = models.CharField(max_length=100)
    sitter_image = models.URLField()
    sitter_phone_number = models.CharField(max_length=12)
    sitter_email = models.EmailField()

    objects = RawReviewManager()

    """
    TODO:
    add owner / sitter fk once tables are populated
    """
    sitter_object = models.ForeignKey(
        Sitter, null=True, on_delete=models.SET_NULL, related_name='raw_reviews')
    owner_object = models.ForeignKey(
        Owner, null=True, on_delete=models.SET_NULL, related_name='raw_reviews')


class Review(AbstractModel):
    """
    Represents a Review of sitter. This table will be populated 1x
    from `RawReview` and then added to for all futher reviews.
    """
    # keys
    sitter = models.ForeignKey(
        Sitter, on_delete=models.CASCADE, related_name='reviews')
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name='reviews')
    # fields
    rating = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    text = models.TextField()
    dogs = models.CharField(max_length=200)
