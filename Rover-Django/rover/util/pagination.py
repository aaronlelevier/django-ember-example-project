import math
from django.conf import settings

from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class RoverPageNumberPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_count', self.get_page_count(self.page.paginator.count)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    @staticmethod
    def get_page_count(count):
        return math.ceil(count/settings.PAGE_SIZE)
