from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from api.serializers import AccountSerializer
from api.models import Account
from django.http import Http404

class AccountView(RetrieveAPIView):

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        try:
            return self.request.user.account
        except Account.DoesNotExist:
            raise Http404('Account not found.')
        

