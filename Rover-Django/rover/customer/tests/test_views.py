import os

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APITestCase

from model_mommy import mommy
from customer.models import Sitter


class IndexViewTests(TestCase):

    def test_can_visit_index_view(self):
        # file not in version contol, so must create pre-test
        fname = os.path.join(settings.TEMPLATES_DIR, 'index.html')
        if not os.path.isfile(fname):
            with open(fname, 'w') as f: pass

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)


class SitterTests(APITestCase):

    def setUp(self):
        self.top_overall_score = 5

        for i in range(1, self.top_overall_score+1):
            mommy.make(Sitter, ratings_score=i/2., overall_score=i)

    def test_list(self):
        sitter = Sitter.objects.order_by('-overall_score')[0]

        response = self.client.get('/api/sitters/')

        self.assertEqual(response.status_code, 200, response.data)
        data = response.data
        self.assertEqual(data['count'], 5)
        self.assertEqual(data['results'][0]['id'], str(sitter.id))
        self.assertEqual(data['results'][0]['name'], sitter.name)
        self.assertEqual(data['results'][0]['image'], sitter.image)
        self.assertEqual(data['results'][0]['ratings_score'], sitter.ratings_score)

        # default ordering is by Sitter overall_score descending
        self.assertEqual(sitter.overall_score, self.top_overall_score)

    def test_search_by_name(self):
        sitter = mommy.make(Sitter, name='foo')
        sitter2 = mommy.make(Sitter, name='fooooo')
        sitter3 = mommy.make(Sitter, name='bar')

        response = self.client.get('/api/sitters/?name={}'.format('foo'))

        self.assertEqual(response.status_code, 200, response.data)
        data = response.data
        self.assertEqual(data['count'], 2)
        sitter_names = [x['name'] for x in data['results']]
        self.assertIn(sitter.name, sitter_names)
        self.assertIn(sitter2.name, sitter_names)

    def test_sort_by_name(self):
        response = self.client.get('/api/sitters/?ordering={}'.format('name'))

        self.assertEqual(response.status_code, 200, response.data)
        data = response.data
        self.assertTrue(data['results'][0]['name'] < data['results'][1]['name'])

    def test_sort_by_ratings_score(self):
        response = self.client.get('/api/sitters/?ordering={}'.format('ratings_score'))

        self.assertEqual(response.status_code, 200, response.data)
        data = response.data
        self.assertTrue(
            data['results'][0]['ratings_score'] < data['results'][1]['ratings_score'])

    def test_filter_by_min_ratings_score(self):
        min_ratings_score = 2

        response = self.client.get('/api/sitters/?min_ratings_score={}'.format(
            min_ratings_score))

        self.assertEqual(response.status_code, 200, response.data)
        data = response.data
        self.assertEqual(
            data['count'],
            Sitter.objects.filter(ratings_score__gte=min_ratings_score).count())
        for d in data['results']:
            self.assertTrue(
                d['ratings_score'] >= min_ratings_score,
                '{} >= {} not True'.format(d['ratings_score'], min_ratings_score))
