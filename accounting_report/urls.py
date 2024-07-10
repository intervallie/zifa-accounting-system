from django.urls import path
from .views import neraca_report, labarugi_report, report_landing_page

app_name = 'report'
urlpatterns = [
    path('report/', report_landing_page, name='report_landing_page'),
    path('neraca/<str:end_date>/', neraca_report, name='neraca_report'),
    path('labarugi/<str:start_date>/<str:end_date>/', labarugi_report, name='labarugi_report'),
]
