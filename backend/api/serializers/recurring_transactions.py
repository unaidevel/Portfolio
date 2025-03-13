from rest_framework import serializers
from api.serializers.goals import GoalsSerializer
from api.models import RecurringTransaction, Goals, Category, Budget
class Recurring_TransactionSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goals = GoalsSerializer(many=True, read_only=True)

    class Meta:
        model = RecurringTransaction
        fields = ['id', 'user', 'amount', 'category', 'description', 'budget', 'goals', 'transaction_type', 'start_date', 
            'frequency_time', 'next_due_date']
        read_only_fields = ['id']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            self.fields['goals'].queryset = Goals.objects.filter(user=request.user)
            self.fields['category'].queryset = Category.objects.filter(user=request.user)
            self.fields['budget'].queryset = Budget.objects.filter(user=request.user)


        