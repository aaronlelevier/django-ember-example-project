from django.core.management.base import BaseCommand

from review.models import RawReview


class Command(BaseCommand):
    help = "Populates the RawReview table from the reviews.csv file"

    def handle(self, **options):
        RawReview.objects.populate()
