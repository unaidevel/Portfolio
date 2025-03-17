from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, Account, Budget
from django.contrib.auth.models import User


#Update the budget when transaction is created
@receiver(post_save, sender=Transaction)
def update_budget_and_account_on_save(sender, instance, **kwargs):
    update_budget_and_account(instance)

# Update budget when a transaction is deleted
@receiver(post_delete, sender=Transaction)
def update_budget_and_account_on_delete(sender, instance, **kwargs):
    update_budget_and_account(instance)

def update_budget_and_account(instance):
    #update remaining budget
    if instance.budget:
        instance.budget.update_remaining_budget()
    

    if hasattr(instance.user, 'account'):
        instance.user.account.update_balance()


    if instance.goal:
        instance.goal.current_amount += instance.amount
        instance.goal.update_status()
        instance.goal.save()

# Create user account when user is created
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

# Save user account when the user is saved
@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()


@receiver(post_save, sender=Budget)
def budget_saved(sender, instance, **kwargs):
    instance.check_budget_threshold()