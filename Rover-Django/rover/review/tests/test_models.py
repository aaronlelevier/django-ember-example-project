from django.test import TestCase
from model_mommy import mommy

from customer.models import Owner, Sitter
from review.models import RawReview, RawReviewManager, Review, ReviewManager


class RawReviewManagerTests(TestCase):

    def test_populate(self):
        self.assertEqual(RawReview.objects.count(), 0)

        RawReview.objects.populate()

        self.assertEqual(RawReview.objects.count(), 500)

    def test_populate__raise_error_if_already_populated(self):
        mommy.make(RawReview)
        count = RawReview.objects.count()

        self.assertEqual(count, 1)

        with self.assertRaisesRegexp(
            AssertionError,
            'RawReview is alredy populated with {} records'.format(count)):

            RawReview.objects.populate()

    def test_set_owner_and_sitter_fks(self):
        RawReview.objects.populate()
        Owner.objects.populate()
        Sitter.objects.populate()

        RawReview.objects.set_owner_and_sitter_fks()

        # owner
        self.assertFalse(
            RawReview.objects.filter(owner_object__isnull=True).exists())
        owner_data = Owner.objects.values_list('id', flat=True)
        owner_raw_review_data = RawReview.objects.values_list(
            'owner_object__id', flat=True)
        self.assertFalse(set(owner_data) ^ set(owner_raw_review_data))
        # sitter
        self.assertFalse(
            RawReview.objects.filter(sitter_object__isnull=True).exists())
        sitter_data = Sitter.objects.values_list('id', flat=True)
        sitter_raw_review_data = RawReview.objects.values_list(
            'sitter_object__id', flat=True)
        self.assertFalse(set(sitter_data) ^ set(sitter_raw_review_data))


class RawReviewTests(TestCase):

    def test_manager(self):
        self.assertIsInstance(RawReview.objects, RawReviewManager)


class ReviewManagerTests(TestCase):

    def test_populate(self):
        RawReview.objects.populate()
        Owner.objects.populate()
        Sitter.objects.populate()
        RawReview.objects.set_owner_and_sitter_fks()

        Review.objects.populate()

        self.assertEqual(
            RawReview.objects.count(), Review.objects.count())


class ReviewTests(TestCase):

    def test_manager(self):
        self.assertIsInstance(Review.objects, ReviewManager)
