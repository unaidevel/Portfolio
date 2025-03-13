# from django.db import models
# import uuid
# from django.contrib.auth.models import User

# class SpendingSummary(models.Model):

#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)
#     total_spent = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.ForeignKey('Category', on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ['user', 'date', 'category']