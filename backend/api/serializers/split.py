from rest_framework import serializers
from api.models import SplitTransaction


class SplitSerializer(serializers.ModelSerializer):

    class Meta:
        model = SplitTransaction
        fields = ['id', 'parent_transaction', 'category', 'amount']
        read_only_fields = ['id']

