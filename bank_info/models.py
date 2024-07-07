from django.db import models

# Create your models here.

class BankInfo(models.Model):
    name = models.CharField(max_length=100)
    is_bankcrupt = models.BooleanField(default=False)

    def __str__(self):
        return self.name