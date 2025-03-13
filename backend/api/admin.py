from django.contrib import admin
from api.models import Category, Transaction, Budget, RecurringTransaction

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(RecurringTransaction)