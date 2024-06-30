from django.urls import path
from .views import account_list, account_create, account_update, account_delete

app_name = 'charts_of_account'
urlpatterns = [
    path('', account_list, name='account_list'),
    path('create/', account_create, name='account_create'),
    path('update/<str:pk>/', account_update, name='account_update'),
    path('delete/<str:pk>/', account_delete, name='account_delete'),
]
