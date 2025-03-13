from rest_framework import serializers
from api.serializers import CategorySerializer
from api.serializers.split import SplitSerializer
from rest_framework import exceptions
from api.models import Goals, Category, Budget, Transaction, RecurringTransaction, SplitTransaction


class TransactionSerializer(serializers.ModelSerializer):

    splits = SplitSerializer(many=True, required=False)

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    external_category = CategorySerializer(many=True, read_only=True)
    goal = serializers.PrimaryKeyRelatedField(queryset=Goals.objects.none(), required=False, allow_null=True)   #None(): Returning an empty list so we can add the elements we desire.
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none())
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'transaction_type', 'splits', 'goal', 'budget', 'amount', 'date_created',
        'external_category']
        read_only_fields = ['id']
        
    def __init__(self, *args, **kwargs):     #Required to get user queryset instead of returning everything. 
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            self.fields['goal'].queryset = Goals.objects.filter(user=request.user)
            self.fields['category'].queryset = Category.objects.filter(user=request.user)
            self.fields['budget'].queryset = Budget.objects.filter(user=request.user)

    # def create(self, validated_data):
    #     validated_data['user'] = self.context['request'].user
    #     return super().create(validated_data)
    

    def create(self, validated_data):
        splits_data = validated_data.pop('splits', None)
        transaction = Transaction.objects.create(**validated_data)

        if splits_data:
            transaction.is_split = True
            transaction.save()
            for split in splits_data:
                SplitTransaction.objects.create(parent_transaction=transaction, **split)
        return transaction
    

        
    def create(self, validated_data):
        splits_data = validated_data.pop('splits', None)
        transaction = Transaction.objects.create(**validated_data)

        if splits_data:
            transaction.is_split = True
            transaction.save()
            for split in splits_data:
                SplitTransaction.objects.create(parent_transaction=transaction, **split)
        
        return transaction
        
    # def validate_goal(self, value):
    #     if self.context['request'].user != value:
    #         raise serializers.ValidationError('You can only see your own goals!')
    #     return value