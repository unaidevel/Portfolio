from django.db import models
from django.contrib.auth.models import User

# class Account(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     balance = models.DecimalField(max_digits=10, decimal_places=2)

#     def update_balance(self):
#         total_income = Transaction.objects.filter(user=self.user, amount__gt=0).aggregate(total=Sum('amount'))['total'] or 0
#         total_expense = Transaction.objects.filter(user=self.user, amount__lt=0).aggregate(total=Sum('amount'))['total'] or 0

#         self.balance = total_income - total_expense
#         self.save()

#     def __str__(self):
#         return f'Account of{self.user.username}. Balance: {self.balance}'
    


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_balance(self):
        transactions = self.user.transaction_set.all()
        income = transactions.filter(transaction_type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
        expense = transactions.filter(transaction_type='expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
        self.balance = income - expense
        self.save()

    def __str__(self):
        return f'Account of {self.user.username} with balance {self.balance}'
    
