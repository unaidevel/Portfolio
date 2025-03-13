from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.exceptions import ValidationError

from .transaction import Transaction

class Budget(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(max_length=500, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Budget: {self.name} for {self.total_amount}. Remaining:{self.remaining_budget}'

    
    def clean(self):
        if self.remaining_budget < 0:
            raise ValidationError({"remaining_budget": "Remaining budget cannot be negative"})
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.remaining_budget = self.total_amount
        super().save(*args, **kwargs)


    def update_remaining_budget(self):
        transactions = Transaction.objects.filter(budget=self)
        total_spent = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        self.remaining_budget = self.total_amount - total_spent
        self.save()



