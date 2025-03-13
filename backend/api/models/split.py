from django.db import models
import uuid


class SplitTransaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    parent_transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name='splits')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
