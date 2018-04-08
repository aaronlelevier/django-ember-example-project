from rest_framework import serializers

from customer.models import Sitter


class SitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitter
        fields = ('id', 'name', 'image', 'ratings_score')
