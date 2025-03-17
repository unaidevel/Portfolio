from django.db import models
import uuid
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from .transaction import Transaction
from django.utils import timezone




class Goals(models.Model):

    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    EXPIRED = 'expired'

    STATUS_CHOICES = [
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (EXPIRED, 'Expired'),
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_time_edited = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default=IN_PROGRESS, max_length=12)

    def process_percentage(self):
        return (self.current_amount / self.target_amount) * 100 if self.target_amount > 0 else 0
    
    def __str__(self):
        return f'Goal: {self.name}. Current amount: {self.current_amount}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.current_amount = self.target_amount
        self.update_status()
        super().save(*args, **kwargs)

    def clean(self):
        if self.current_amount > self.target_amount:
            raise ValidationError("The current amount can't exceed target amount!")
        
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError("The deadline can't exceed")
        
    def update_status(self):
        if self.current_amount >= self.target_amount:
            self.status = self.COMPLETED
        elif self.deadline and self.deadline < timezone.now():
            self.status = self.EXPIRED
        else:
            self.status = self.IN_PROGRESS


