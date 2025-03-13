from django.core.management.base import BaseCommand
from django.utils import timezone
from finances.models import RecurringTransaction, Transaction

class Command(BaseCommand):
    help = 'Process recurring transactions and create corresponding transactions'

    def handle(self, *args, **kwargs):
        now = timezone.now().date()
        recurring_transactions = RecurringTransaction.objects.filter(next_due_date__lte=now)

        for recurring in recurring_transactions:
            Transaction.objects.create(
                user=recurring.user,
                category = recurring.category,
                amount = recurring.amount,
                transaction_type=recurring.transaction_type,
                budget = recurring.budget,
                date_created = now,
            )
            
            recurring.next_due_date = recurring.calculate_next_due_date()
            recurring.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully processed recurring transactions'))
        