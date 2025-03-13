from rest_framework import serializers
from api.models import Budget, Category
from django.utils import timezone



class BudgetSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    create_date = serializers.HiddenField(default=timezone.now)

    class Meta:
        model = Budget 
        fields = ['id', 'name','total_amount','remaining_budget','description', 'category', 'user', 'create_date', 'end_date']
        read_only_fields = ['id', 'remaining_budget']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            self.fields['category'].queryset = Category.objects.filter(user=request.user)


    
    # def validate_user(self, value):
    #     if self.context['request'].user != value:
    #         raise serializers.ValidationError('You can only create budget for yourself')
    #     return value
    

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    


