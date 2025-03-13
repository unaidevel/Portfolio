from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from finances.models import Transaction, Category

# class TransactionTests_Session_Auth(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.category = Category.objects.create(name='Salary', category_type='income')
#         self.client.login(username='testuser', password='testpass')

#     def test_create_transaction_session_auth(self):
#         data = {
#             'user': self.user.id,
#             'category': self.category.id,
#             'transaction_type': 'income',
#             'amount': 1000,
#         }
#         response = self.client.post('/transaction/', data)
#         self.assertEqual(response.status_code, 201)

    
    # def test_create_category(self):
    #     pass



from rest_framework.authtoken.models import Token
class TransactionTests_Token_Auth(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='password')
        self.category = Category.objects.create(name='chicken food', category_type='expense')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_transaction(self):
        data = {
            'user': self.user.id,
            'category': self.category.id,
            'transaction_type': 'income',
            'amount': 1000,
        }
        response = self.client.post('/transaction/', data)
        self.assertEqual(response.status_code, 201)
