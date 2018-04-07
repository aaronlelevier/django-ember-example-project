from django.core.management.base import BaseCommand

from customer.models import Owner, Sitter
from review.models import RawReview, Review


class Command(BaseCommand):
    help = "Initial populate for all database table"

    def handle(self, **options):
        RawReview.objects.populate()
        Owner.objects.populate()
        Sitter.objects.populate()
        RawReview.objects.set_owner_and_sitter_fks()
        Review.objects.populate()
        Sitter.objects.set_scores()
