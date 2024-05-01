from django.db import models
from charts_of_account.models import ChartsOfAccount

# Create your models here.
class Journal(models.Model):
    journal_num = models.CharField(max_length=10, primary_key=True)
    journal_date = models.DateField()
    desc = models.TextField(null=True)
    credit_sum = models.IntegerField(null=True)
    debit_sum = models.IntegerField(null=True)

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('KRD', 'Kredit'),
        ('DBT', 'Debit')
    ]
    acc_code = models.ForeignKey(ChartsOfAccount, on_delete=models.CASCADE)
    journal_code = models.ForeignKey(Journal, on_delete=models.CASCADE)
    trans_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES)
    value = models.IntegerField(null=True)