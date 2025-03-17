from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

TRANSACTION_TYPES = [
    ('income', 'Income'),
    ('expense', 'Expense'),
]

class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, default=None, max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    goal = models.ForeignKey('Goals', on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    split = models.BooleanField(default=False)


    def __str__(self):
        return f'Transaction of {self.amount} done.'
    


    

# @receiver (post_save, sender=Transaction)
# def update_account_balance(sender, instance, **kwargs):
#     instance.user.account.update_balance()





