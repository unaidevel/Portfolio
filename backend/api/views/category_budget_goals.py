from rest_framework import viewsets
from api.models import Category, Budget, Goals
from api.serializers import CategorySerializer, BudgetSerializer, GoalsSerializer
from api.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
class CategoryViewSet(viewsets.ModelViewSet):

    # authentication_classes = [JWTAuthentication]
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


    def get_queryset(self):
        transaction_type = self.request.query_params.get('transaction_type', None)

        queryset = Category.objects.filter(user=self.request.user)
        if transaction_type:
            queryset = queryset.filter(category_type=transaction_type)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    


class BudgetView(viewsets.ModelViewSet):

    # authentication_classes = [JWTAuthentication]
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Budget.objects.all()

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    

    @action(detail=True, methods=['GET'])
    def transactions(self, request, pk=None):
        budget = self.get_object()
        transacations = budget.transactions.all()
        serializer = TransactionSerializer(transacations, many=True)
        return Response(serializer.data)
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class GoalsView(viewsets.ModelViewSet):

    # authentication_classes = [JWTAuthentication]
    serializer_class = GoalsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Goals.objects.all()

    def get_queryset(self):
        return Goals.objects.filter(user=self.request.user)

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)





