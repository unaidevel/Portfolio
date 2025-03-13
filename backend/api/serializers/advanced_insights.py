from rest_framework import serializers


# Created this for new views. Avoiding using old serializers.
class AdvancedInsightsSerializer(serializers.Serializer):

    total_spent_per_month = serializers.ListField(child=serializers.DictField())
    total_sum = serializers.DictField()
    yearly_spending = serializers.ListField()
    top_spent_categories = serializers.ListField()
    transaction_count_per_category = serializers.ListField()
    upcoming_recurring_transactions = serializers.ListField()