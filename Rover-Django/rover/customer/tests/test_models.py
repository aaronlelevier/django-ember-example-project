from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models import Sum, Count, Avg

from model_mommy import mommy

from customer.models import Owner, OwnerManager, Sitter, SitterManager
from review.models import RawReview, Review


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


class SitterManagerScoreTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SitterManagerScoreTests, cls).setUpClass()

        RawReview.objects.populate()
        Owner.objects.populate()
        Sitter.objects.populate()
        RawReview.objects.set_owner_and_sitter_fks()
        Review.objects.populate()

        Sitter.objects.set_scores()

    def test_set_scores__stays(self):
        sitter_stays = Sitter.objects.all().aggregate(total=Sum('stays'))
        self.assertEqual(Review.objects.count(), sitter_stays['total'])

    def test_set_scores__ratings_score(self):
        sitter = Sitter.objects.first()
        sitter_reviews = Review.objects.filter(sitter=sitter)
        stays = sitter_reviews.count()
        total_ratings = sitter_reviews.aggregate(total=Sum('rating'))['total']
        self.assertFloatEqual(sitter.ratings_score, total_ratings/stays)

    def test_set_scores__sitter_score(self):
        sitter = Sitter.objects.first()

        self.assertFloatEqual(
            sitter.sitter_score,
            (sum(1 for let in {s.lower() for s in sitter.name} if let.isalpha()) / 26)*5)

    def test_set_scores__overall_score(self):
        self.assertFloatEqual(
            Sitter.objects.all().aggregate(total=Sum('overall_score'))['total'],
            sum(s.calc_overall_score() for s in Sitter.objects.all())
        )

    def assertFloatEqual(self, f1, f2):
        self.assertEqual(
            "{:.4f}".format(f1), "{:.4f}".format(f2))


class SitterTests(TestCase):

    def test_manager(self):
        self.assertIsInstance(Sitter.objects, SitterManager)

    def test_calc_sitter_score(self):
        sitter = mommy.make(Sitter)

        self.assertEqual(
            sitter.calc_sitter_score(),
            (sum(1 for let in {s for s in sitter.name.lower()} if let.isalpha()) / 26)*5
        )

    def test_calc_overall_score(self):
        for i in range(13):
            sitter = mommy.make(Sitter, stays=i, ratings_score=5, sitter_score=2.5)
            if i == 0:
                self.assertEqual(sitter.calc_overall_score(), sitter.sitter_score)
            elif i >=10:
                self.assertEqual(sitter.calc_overall_score(), sitter.ratings_score)
            else:
                self.assertEqual(sitter.calc_overall_score(), i*.25 + sitter.sitter_score)


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
