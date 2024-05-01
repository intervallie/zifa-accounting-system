from django.db import models

# Create your models here.
class ChartsOfAccount(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('KB', 'Kas & Bank'),
        ('PU', 'Piutang Usaha'),
        ('Per', 'Persediaan'),
        ('ALL', 'Aset Lancar Lainnya'),
        ('AT', 'Aset Tetap'),
        ('AP', 'Akumulasi Penyusutan'),
        ('AL', 'Aset Lainnya'),
        ('UU', 'Utang Usaha'),
        ('LJPe', 'Liabilitas Jangka Pendek'),
        ('LJPa', 'Liabilitas Jangka Panjang'),
        ('M', 'Modal'),
        ('Pen', 'Pendapatan'),
        ('BPP', 'Beban Pokok Penjualan'),
        ('B', 'Beban'),
        ('BL', 'Beban Lainnya'),
        ('PL', 'Pendapatan Lainnya')
    ]
    code = models.CharField(max_length=10, primary_key=True)
    parent_account = models.ForeignKey('self', on_delete=models.CASCADE,
                                       null=True)
    account_type = models.CharField(max_length=4, choices=ACCOUNT_TYPE_CHOICES)
    account_name = models.CharField(max_length=100)
    balance = models.IntegerField(null=True, default=0)
    notes = models.TextField(blank=True)

