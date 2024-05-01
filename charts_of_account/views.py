from django.shortcuts import render, redirect, get_object_or_404
from .models import ChartsOfAccount

def account_list(request):
    accounts = ChartsOfAccount.objects.all()
    parent_accounts = [(account.code, account.account_name) for account in accounts]
    return render(request, 'account_list.html', {'accounts': accounts, 'parent_accounts': parent_accounts})

def account_create(request):
    if request.method == 'POST':
        # Extracting parameters from the GET request
        code = request.POST.get('code')
        parent_account_code = request.POST.get('parent_account')
        account_type = request.POST.get('account_type')
        account_name = request.POST.get('account_name')
        balance = request.POST.get('balance')
        notes = request.POST.get('notes')

        # Retrieve parent account if exists
        parent_account = None
        if parent_account_code:
            parent_account = get_object_or_404(ChartsOfAccount, code=parent_account_code)

        # Create a new ChartsOfAccount instance using the extracted data
        ChartsOfAccount.objects.create(
            code=code,
            parent_account=parent_account,
            account_type=account_type,
            account_name=account_name,
            balance=balance,
            notes=notes
        )

        return redirect('account_list')

    existing_accounts = ChartsOfAccount.objects.all()
    parent_accounts = [(account.code, account.account_name) for account in existing_accounts]
    return render(request, 'account_form.html', {'parent_accounts': parent_accounts})

def account_update(request, pk):
    account = get_object_or_404(ChartsOfAccount, pk=pk)
    if request.method == 'POST':
        # Extracting parameters from the GET request
        account.code = request.POST.get('code')
        parent_account_code = request.POST.get('parent_account')
        account.account_type = request.POST.get('account_type')
        account.account_name = request.POST.get('account_name')
        account.balance = request.POST.get('balance')
        account.notes = request.POST.get('notes')

        # Retrieve parent account if exists
        if parent_account_code:
            parent_account = get_object_or_404(ChartsOfAccount, code=parent_account_code)
            account.parent_account = parent_account
        else:
            account.parent_account = None

        # Save the updated ChartsOfAccount instance
        account.save()

        return redirect('account_list')

    return render(request, 'account_form.html')

def account_delete(request, pk):
    account = get_object_or_404(ChartsOfAccount, pk=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('account_list')
    return render(request, 'account_confirm_delete.html', {'account': account})
