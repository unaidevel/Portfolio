from rest_framework import serializers
from api.models import Goals, Category

class GoalsSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goals
        fields = ['id', 'name', 'description', 'target_amount', 'current_amount', 'deadline', 
                  'date_created', 'last_time_edited', 'category', 'user', 'status']
        read_only_fields = ['id', 'date_created', 'status', 'current_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            self.fields['category'].queryset = Category.objects.filter(user=request.user)
