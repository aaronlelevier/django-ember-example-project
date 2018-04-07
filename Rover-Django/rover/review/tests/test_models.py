from django.test import TestCase

from model_mommy import mommy
from review.models import RawReview, RawReviewManager


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


class RawReviewTests(TestCase):

    def test_manager(self):
        self.assertIsInstance(RawReview.objects, RawReviewManager)
