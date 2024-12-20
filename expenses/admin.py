from django.contrib import admin
from .models import *
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'category','date')
    search_fields = ('description', 'category','date')
    list_per_page=5


admin.site.register(Expenses,ExpenseAdmin)
admin.site.register(Category)