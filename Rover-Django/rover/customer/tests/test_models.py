from django.contrib.auth.models import User
from django.test import TestCase

from customer.models import Owner, OwnerManager, Sitter, SitterManager
from review.models import RawReview


class SitterManagerTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SitterManagerTests, cls).setUpClass()

        RawReview.objects.populate()

    def test_populate(self):
        self.assertEqual(Sitter.objects.count(), 0)

        Sitter.objects.populate()

        expected_count = 100
        self.assertEqual(User.objects.count(), expected_count)
        self.assertEqual(User.objects.filter(email__isnull=True).count(), 0)
        self.assertEqual(Sitter.objects.count(), expected_count)


class SitterTests(TestCase):

    def test_manager(self):
        self.assertIsInstance(Sitter.objects, SitterManager)


class OwnerManagerTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(OwnerManagerTests, cls).setUpClass()

        RawReview.objects.populate()

    def test_populate(self):
        self.assertEqual(Owner.objects.count(), 0)

        Owner.objects.populate()

        expected_count = 189
        self.assertEqual(User.objects.count(), expected_count)
        self.assertEqual(User.objects.filter(email__isnull=True).count(), 0)
        self.assertEqual(Owner.objects.count(), expected_count)


class OwnerTests(TestCase):

    def test_manager(self):
        self.assertIsInstance(Owner.objects, OwnerManager)
