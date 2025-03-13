from django.db import models
import uuid
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from api.models import Transaction

TRANSACTION_TYPES = [
    ('income', 'Income'),
    ('expense', 'Expense'),
]


FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
]

class RecurringTransaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='Recurring_transaction')
    description = models.CharField(max_length=100)
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE, related_name='Recurring_transaction', null=True, blank=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=15)  # Corrected this line
    start_date = models.DateField(auto_now_add=True)
    frequency_time = models.CharField(choices=FREQUENCY_CHOICES, default=None, max_length=15)
    next_due_date = models.DateField()

    def __str__(self):
        return f'Recurring transaction of {self.category} created.'
    
    def save(self, *args, **kwargs):
        if not self.next_due_date:
            self.next_due_date = self.calculate_next_due_date()
        super().save(*args, **kwargs)
    
    def calculate_next_due_date(self):
        if self.frequency == 'daily':
            return self.start_date + timezone.timedelta(days=1)
        elif self.frequency == 'weekly':
            return self.start_date + timezone.timedelta(weeks=1)
        elif self.frequency == 'monthly':
            return self.start_date + timezone.timedelta(weeks=4, days=2)
        return self.start_date

    def generate_transaction_from_recurring(Recurring_Transaction):
        transaction = Transaction.objects.create(
            user=Recurring_Transaction.user,
            amount=Recurring_Transaction.amount,
            transaction_type=Recurring_Transaction.transaction_type,
            date=timezone.now())

        transaction.user.account.update_balance()


