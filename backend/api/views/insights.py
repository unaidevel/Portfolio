from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from api.models import Transaction, RecurringTransaction, Budget
from api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.response import Response
from api.serializers import AdvancedInsightsSerializer, TransactionSerializer
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncMonth, TruncYear
from datetime import datetime, timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication


class SpendingListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by('-date_created')

# class InsightList(ListAPIView):

#     serializer_class = SpendingInsightSerializer
#     permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Transaction.objects.filter(user=user).order_by('-date_created')


class MonthlySpendingView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request, *args, **kwargs):
        pass




# class ExerciseView(ListAPIView):
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

#     def list(self, request, *args, **kwargs):
#         # total spent by a specific user
#         user = request.user
#         total_spent = Transaction.objects.filter(user=user).aggregate(Sum('amount'))
#         return Response(total_spent)


# class ExerciseView(ListAPIView):
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

#     def list(self, request, *args, **kwargs):
#         total_spent_category = Transaction.objects.filter(user=request.user).values('category__name').annotate(total_spent=Sum('amount'))
#         return Response(total_spent_category)



class InsightsView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        total_spent_category = Transaction.objects.filter(user=request.user).values('category__name').annotate(total_spent=Sum('amount'))
        average_spent_category = Transaction.objects.filter(user=request.user).values('category__name').annotate(average_spent=Avg('amount'))
        data = [
            {
            'category': item['category__name'],
            'total_spent': item['total_spent'],
            'average spent': tem['average_spent']
        }
        for item in total_spent_category
        for tem in average_spent_category
        ]
        serializer = AdvancedInsightsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    


class AdvancedInsights(ListAPIView):


    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request, *args, **kwargs):
        total_spent_per_month = Transaction.objects.filter(user=request.user).values(month=TruncMonth('date_created')).annotate(total_spent=Sum('amount'))
        total_sum = Transaction.objects.filter(user=request.user).aggregate(total_transactions=Sum('amount'))
        yearly_spending = Transaction.objects.filter(user=request.user).values(year=TruncYear('date_created')).annotate(total_spent=Sum('amount'))
        top_spent_categories = Transaction.objects.filter(user=request.user).values('category__name').annotate(total_spent=Sum('amount')).order_by('-total_spent')[:5]
        transaction_count_per_category = Transaction.objects.filter(user=request.user).values('category__name').annotate(total_count=Count('id'))
        upcoming_recurring_transactions = RecurringTransaction.objects.filter(user=request.user, start_date__gte=datetime.now(), start_date__lte=datetime.now() + timedelta(days=30))
        data = {
            'total_spent_per_month': total_spent_per_month,
            'total_sum': total_sum,
            'yearly_spending': yearly_spending,   
            'top_spent_categories': top_spent_categories,
            'transaction_count_per_category': transaction_count_per_category,
            'upcoming_recurring_transactions': upcoming_recurring_transactions,
        }
        serializer = AdvancedInsightsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    





"""

Summary of New Insights You Could Add:

    ---Average Spending per Category
    Yearly Spending Breakdown
    Spending Trend (Month-over-Month)
    Top Categories (Most Spent)
    Transaction Count per Category
    Budget vs. Actual Spending
    Spending by Payment Method
    Upcoming Recurring Transactions
    Top Spenders (if multi-user)
    Custom Date Range Spending
    Spend vs. Income
    
"""