from django.shortcuts import redirect, render
from django.urls import reverse

from accounting_system.charts_of_account.models import ChartsOfAccount


# Create your views here.
def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("user_auth:login"))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def neraca_report(request):
    accounts = ChartsOfAccount.objects.all()
    
    return None

def labarugi_report(request):
    return None

