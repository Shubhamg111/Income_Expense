from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', index,name='income'),  
    path('add-income',add_income,name='add-income'),
    path('edit-income/<int:id>',income_edit,name='income-edit'),
    path('income-delete/<int:id>',delete_income,name='income-delete'),
    path('search-income',csrf_exempt(search_income),name='income/search-income'),
    path('income_summary',income_source_summary,name="income_summary"),
    path('income_stats',income_stats_view,name="income-stats"),
#     path('income_export_csv',income_export_csv,name="income-export-csv"),
#     path('income_export_excel',income_export_excel,name="income-export-excel"),
]
