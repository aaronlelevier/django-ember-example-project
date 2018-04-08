from django.shortcuts import render

from rest_framework.generics import ListAPIView

from rest_framework.filters import OrderingFilter

from customer.models import Sitter
from customer.serializers import SitterSerializer


class SitterListAPIView(ListAPIView):

    queryset = Sitter.objects.order_by('-overall_score')
    serializer_class = SitterSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name', 'ratings_score')

    def get_queryset(self):
        """
        The following query params are accepted:

        - name: to do case insensitive filter by 'name'
        - min_ratings_score: to filter by a minimum 'ratings_score'
        """
        qs = super(SitterListAPIView, self).get_queryset()

        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)

        min_ratings_score = self.request.query_params.get('min_ratings_score')
        if min_ratings_score:
            qs = qs.filter(ratings_score__gte=min_ratings_score)

        return qs
