from django import forms
from .models import ChartsOfAccount

class ChartsOfAccountForm(forms.ModelForm):
    class Meta:
        model = ChartsOfAccount
        fields = ['code', 'parent_account', 'account_type', 'account_name', 'balance', 'notes']
