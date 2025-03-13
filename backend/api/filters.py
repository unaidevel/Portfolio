import django_filters
from api.models import Transaction

class TransactionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    amount = django_filters.RangeFilter()


    class Meta:
        model = Transaction
        fields = {
            'amount': ['exact','lt', 'gt', 'gte', 'lte'],
            'date_created': ['exact', 'year__gt', 'year__lte'],
            'category': ['exact'],
        }