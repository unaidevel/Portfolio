from celery import shared_task
from django.utils import timezone
from .models import RecurringTransaction, Transaction

@shared_task
def process_recurring_transactions():
    now = timezone.now().date()
    recurring_transactions = RecurringTransaction.objects.filter(next_due_date__lte=now)
    for recurring in recurring_transactions:
        Transaction.objects.create(
            user=recurring.user,
            category=recurring.category,
            amount=recurring.amount,
            transaction_type=recurring.transaction_type,
            budget=recurring.budget,
            date_created=now,
        )

        recurring.next_due_date = recurring.calculate_next_due_date()
        recurring.save()

@shared_task
def test_task():
    print("Test task executed successfully!")
    return 'Test task executed successfully!'