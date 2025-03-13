from api.models import Account
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):

    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Account
        fields = ['user', 'balance']
        # read_only_fields = ['user', 'balance']
