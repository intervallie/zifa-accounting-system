from django.urls import path
from .views import journal_create, journal_detail, journal_delete, journal_list, journal_update, transaction_create, transaction_delete, transaction_update

urlpatterns = [
    path('', journal_list, name='journal_list'),
    path('journal-detail/<int:journal_num>/', journal_detail, name='journal_detail'),
    path('journal-create/', journal_create, name='journal_create'),
    path('journal-update/<int:journal_num>/', journal_update, name='journal_update'),
    path('journal-delete/<int:journal_num>/', journal_delete, name='journal_delete'),
    path('transaction-create/<int:journal_code>/', transaction_create, name='transaction_create'),
    path('transaction-update/<int:transaction_id>/', transaction_update, name='transaction_update'),
    path('transaction-delete/<int:transaction_id>/', transaction_delete, name='transaction_delete'),
]
