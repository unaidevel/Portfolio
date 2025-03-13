from rest_framework.routers import DefaultRouter
from api import views
from django.urls import path, include 

router = DefaultRouter()
router.register(r'transaction', views.TransactionViewSet, basename='transaction_list')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'budget', views.BudgetView, basename='budget')
router.register(r'recurring_transactions', views.RecurringTransactionView, basename='recurring_transactions')
router.register(r'goals', views.GoalsView, basename='goals')


# urlpatterns = [
#     path('', include(router.urls)),
#     path('spendings', SpendingList.as_view(), name='spending_list')
# ]

urlpatterns = [
    path('', include(router.urls)),
    path('transaction-list/', views.SpendingListView.as_view(), name='spending_list'), #List filtered by date created
    path('advanced-insights/', views.AdvancedInsights.as_view(), name='advanced_insights'),#Total spent per month and total sum
    path('insights-view/', views.InsightsView.as_view(), name='Insights_View'),
    path('account/', views.AccountView.as_view(), name='account_balance'),
]