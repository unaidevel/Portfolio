import csv
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import permissions
from api.models import Transaction, Account
from api.permissions import IsOwnerOrReadOnly
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap




"""Using Django CSV built int method"""
# class Export_transaction_csv(APIView):
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
#     def get(self, request):
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="transcations.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['Date_created', 'Amount', 'Category'])

        
#         transactions = Transaction.objects.filter(user=request.user)

#         for transaction in transactions:
#             writer.writerow([transaction.date_created, transaction.amount, transaction.category])
        
#         return response





class ExportTransactionCsv(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).values('date_created', 'amount',
                                                                           'category')
        df = pd.DataFrame(list(transactions))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
        df.to_csv(response, index=False)

        return response
    

class ExportTransactionExcel(APIView):

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ['get']

    def get(self, request):

        transactions = Transaction.objects.filter(user=request.user).values('date_created','amount','category')

        df = pd.DataFrame(list(transactions)).fillna('')
        response = HttpResponse(content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="transactions.xlsx"'
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Transactions')
        return response
    

class ExportTransactionPdf(APIView):

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ['get']

    def get(self, request):

        transactions = Transaction.objects.filter(user=request.user).values('date_created', 'amount', 
                                                                            'category')
        account_balance = Account.objects.filter(user=request.user).first() #Objective: Return one value or none
        # I created the same with values to balance and it returns a dict, error
                                                                            
        df = pd.DataFrame(list(transactions))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'

        c = canvas.Canvas(response, pagesize=letter) #creates the pdf
        y_position = 750

        if account_balance:
            balance = account_balance.balance
            c.drawString(100, y_position, f'Account Balance: {balance:.2f}')  #:.2f for rounding the number to 2 decimal places, i think its already limited
            y_position -= 40
        c.drawString(100, y_position, 'Transaction List') #title
        y_position -= 20

        for index, row in df.iterrows():   #The only way to create pdf is by making a for to the rows
            y_position -= 20
            if y_position < 40: #Objective: create new page when we reaching the bottom
                c.showPage()
                y_position = 750
            category = str(row['category'])
            wrapped_category = textwrap.fill(category, width=50)  #With widht the lenght of the category number can be edited
            c.drawString(100, y_position, f'Date: {row['date_created']} | Amount: {row['amount']}')
            y_position -= 20
            c.drawString(100, y_position, f'    Category: {wrapped_category}') #Made it separate to show category entirely

        c.save()

        return response

