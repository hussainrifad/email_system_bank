from django.contrib import admin
from .models import Transaction, SendMoney

# Register your models here.

admin.site.register(Transaction)
admin.site.register(SendMoney)