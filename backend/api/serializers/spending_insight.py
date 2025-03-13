# from rest_framework import serializers
# from finances.models.spending_summary import SpendingSummary


# class SpendingInsightSerializer(serializers.ModelSerializer):

#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = SpendingSummary 
#         fields = ['id', 'user', 'category', 'date', 'total_spent']
#         read_only_fields = ['id']