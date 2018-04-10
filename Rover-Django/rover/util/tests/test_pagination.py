from rest_framework.test import APITestCase

from customer.models import Sitter
from model_mommy import mommy
from util.pagination import RoverPageNumberPagination


class RoverPageNumberPaginationTests(APITestCase):

    def test_response_obj_structure(self):
        mommy.make(Sitter)

        response = self.client.get('/api/sitters/')

        self.assertEqual(response.status_code, 200, response.data)
        data = response.data
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['page_count'], 1)
        self.assertIn('results', data)
        self.assertIn('previous', data)
        self.assertIn('next', data)

    def test_get_page_count(self):
        p = RoverPageNumberPagination()
        self.assertEqual(p.get_page_count(count=1), 1)
        self.assertEqual(p.get_page_count(count=10), 1)
        self.assertEqual(p.get_page_count(count=11), 2)
        self.assertEqual(p.get_page_count(count=180), 18)
        self.assertEqual(p.get_page_count(count=181), 19)
