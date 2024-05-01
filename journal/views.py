from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Journal, Transaction
from charts_of_account.models import ChartsOfAccount

def journal_list(request):
    journals = Journal.objects.all()
    return render(request, 'journal_list.html', {'journals': journals})

def journal_detail(request, journal_num):
    journal = get_object_or_404(Journal, pk=journal_num)
    transactions = Transaction.objects.filter(journal_code=journal_num)
    return render(request, 'journal_detail.html', {'journal': journal, 'transactions': transactions})

def journal_create(request):
    #by default credit and debit equal 0
    if request.method == 'POST':
        journal_num = request.POST.get('journal_num')
        journal_date = request.POST.get('journal_date')
        desc = request.POST.get('desc')
        journal = Journal(journal_num=journal_num, journal_date=journal_date, desc=desc, credit_sum=0, debit_sum=0)
        journal.save()
        return redirect('journal_detail', journal_num=journal_num)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def journal_update(request, journal_num):
    #only update journal_date, journal_num, and desc
    journal = get_object_or_404(Journal, pk=journal_num)
    if request.method == 'POST':
        journal.journal_num = request.POST.get('journal_num')
        journal.journal_date = request.POST.get('journal_date')
        journal.desc = request.POST.get('desc')
        journal.save()
        return redirect('journal_detail', journal_num=journal_num)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def journal_delete(request, journal_num):
    journal = get_object_or_404(Journal, pk=journal_num)
    transactions = Transaction.objects.all()

    if request.method == 'POST':
        # iterate all the transaction inside and delete them
        for tr in transactions:
            if tr.journal_code == journal_num:
                account = get_object_or_404(ChartsOfAccount, pk=tr.acc_code)
                if tr.trans_type == 'Kredit':
                    account.balance += tr.value
                else:
                    account.balance -= tr.value
                tr.delete()

        journal.delete()
        return redirect('journal_list')
    
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def transaction_create(request, journal_code):
    if request.method == 'POST':
        acc_code = request.POST.get('acc_code')
        trans_type = request.POST.get('trans_type')
        value = request.POST.get('value')
        
        account_src = get_object_or_404(ChartsOfAccount, pk=acc_code)
        journal = get_object_or_404(Journal, journal_code)

        #Update the balance and credit sum with the new transaction value
        if request.POST.get('trans_type') == 'Kredit':
            account_src.balance -= value
            journal.credit_sum += value
        #Update the balance and credit sum with the new transaction value
        else:
            account_src.balance += value
            journal.debit_sum += value

        trans = Transaction(acc_code=acc_code,
                            journal_code=journal_code,
                            trans_type=trans_type,
                            value=value)
        trans.save()
        return redirect('journal_detail', journal_num=journal.journal_num)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def transaction_update(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    account_src = get_object_or_404(ChartsOfAccount, pk=transaction.acc_code)
    account_dest = get_object_or_404(ChartsOfAccount, pk=request.POST.get('acc_code'))
    journal = get_object_or_404(Journal, pk=transaction.journal_code)
    if request.method == 'POST':
        #The previous transaction value will be added into account balance, but will be reduced the journal credit value
        if transaction.trans_type == 'Kredit':
            account_src.balance += transaction.value
            journal.credit_sum -= transaction.value
        #The previous transaction value will be added into account balance, but will be reduced the journal credit value
        else:
            account_src.balance -= transaction.value
            journal.debit_sum -= transaction.value
        
        #Update the balance and credit sum with the new transaction value
        if request.POST.get('trans_type') == 'Kredit':
            account_dest.balance -= transaction.value
            journal.credit_sum += transaction.value
        #Update the balance and credit sum with the new transaction value
        else:
            account_dest.balance += transaction.value
            journal.debit_sum += transaction.value

        transaction.acc_code = request.POST.get('acc_code')
        transaction.trans_type = request.POST.get('trans_type')
        transaction.value = request.POST.get('value')

        transaction.save()
        return redirect('journal_detail', journal_num=journal.journal_num)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def transaction_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    account = get_object_or_404(ChartsOfAccount, pk=transaction.acc_code)
    journal = get_object_or_404(Journal, pk=transaction.journal_code)

    if request.method == 'POST':
        #When delete, transaction value will be added into account balance, but will be reduced the journal credit value
        if transaction.trans_type == 'Kredit':
            account.balance += transaction.value
            journal.credit_sum -= transaction.value
        #When delete, transaction value will be added into account balance, but will be reduced the journal credit value
        else:
            account.balance -= transaction.value
            journal.debit_sum -= transaction.value
        transaction.delete()
        return redirect('journal_detail', journal_num=journal.journal_num)

    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})