from rest_framework import viewsets
from api.serializers import TransactionSerializer, Recurring_TransactionSerializer
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from api.filters import TransactionFilter
from api.models import Transaction, Category, RecurringTransaction
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication



class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TransactionFilter
    filterset_fields = ['amount']
    search_fields = ['amount','category__name']
    ordering_fields = ['amount', 'date_created']
    

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    

    def create(self, request, *args, **kwargs):
        transaction_type = request.data.get('transaction_type')
        category_id = request.data.get('category')
    
        if not Category.objects.filter(id=category_id, category_type=transaction_type).exists():
            return Response(
                {"detail": "Invalid category for the selected transaction type"},
                status=400
            )
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def filter_by_type(self, request):
        transaction_type = request.query_params.get('transaction_type', None)
        if transaction_type:
            transactions = self.get_queryset().filter(transaction_type=transaction_type)
        else:
            transactions = self.get_queryset()
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    

    def list(self, request, *args, **kwargs):
        print(request.user)
        transactions = Transaction.objects.filter(user=request.user)
        return Response(transactions.values())
    



class RecurringTransactionView(viewsets.ModelViewSet):
    serializer_class = Recurring_TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = RecurringTransaction.objects.all()

    def get_queryset(self):
        return RecurringTransaction.objects.filter(user=self.request.user)
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    

    def create(self, request, *args, **kwargs):
        transaction_type = request.data.get('transaction_type')
        category_id = request.data.get('category')

        if not Category.objects.filter(id=category_id, category_type=transaction_type).exists():
            return Response(
                {"detail": "Invalid category for the selected transaction type"},
                status=400
            )
        return super().create(request, *args, **kwargs)