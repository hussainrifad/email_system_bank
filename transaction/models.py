from django.db import models
from user_auth.models import UserBankAccount
from .constants import TRANSACTION_TYPE
# Create your models here.

class Transaction(models.Model):
    account = models.ForeignKey(UserBankAccount, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_approve = models.BooleanField(default=False) 

    def __str__(self):
        return self.account.user.first_name

class SendMoney(Transaction):
    send_to = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name='money_sender')
