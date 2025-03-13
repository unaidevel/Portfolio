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
        



# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# message = Mail(
#     from_email = '',
#     to_email = '',
#     subject = '',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)
