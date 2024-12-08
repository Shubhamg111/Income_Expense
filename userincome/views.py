from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from userpreference.models import *
from django.contrib import messages
import json
from django.http import JsonResponse
from userpreference.models import *
import csv
from django.http import HttpResponse
import xlwt
import datetime


# Create your views here.

def search_income(request):
    if request.method == 'POST': 
        search_str = json.loads(request.body).get('searchText')

        income = UserIncome.objects.filter(amount__istartswith=search_str,owner=request.user) | UserIncome.objects.filter(date__istartswith=search_str,owner=request.user) | UserIncome.objects.filter(description__icontains=search_str,owner=request.user) | UserIncome.objects.filter(source__icontains=search_str,owner=request.user)

    data = income.values()

    return JsonResponse(list(data),safe=False)



@login_required(login_url='/authentication/login')
def index(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner= request.user)
    paginator = Paginator(income,4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    currency = UserPreference.objects.get(user = request.user).currency
    context={
       
        'income':income,
        'page_obj':page_obj,
        'currency':currency

    }
    return render(request,'income/index.html',context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context={
        'sources':sources,
        'values':request.POST
    }
    if request.method == 'GET':
        return render(request,'income/add_income.html',context)

    if request.method == "POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Please fill in the amount field')
            return render(request,'income/add_income.html')
            
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']


        if not description:
            messages.error(request, 'Please fill in the description field')
            return render(request,'income/add_income.html')
        
        UserIncome.objects.create(owner = request.user,amount=amount,date=date,source=source,description=description)
        messages.success(request, 'Income added successfully')
        return redirect('income')


@login_required(login_url='/authentication/login')
def income_edit(request,id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()

    context = {
        'income':income,
        'values': income,
        'sources':sources,

    }
    if request.method == 'GET':
        return render(request,'income/edit-income.html',context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Please fill in the amount field')
            return render(request,'income/edit-income.html')
            
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']


        if not description:
            messages.error(request, 'Please fill in the description field')
            return render(request,'income/edit-income.html')
        
        
        income.owner = request.user
        income.amount=amount
        income.date=date
        income.source=source
        income.description=description
        income.save()
        messages.success(request, 'income saved successfully')
        return redirect('income')
    
    else:
        messages.info(request,'Handling Post Form')
        return render(request,'income/edit-income.html',context)

@login_required(login_url='/authentication/login')
def delete_income(request,id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted successfully')
    return redirect('income')

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_month_ago = todays_date-datetime.timedelta(days=30*6)
    incomes = UserIncome.objects.filter(owner = request.user,date__gte=six_month_ago,date__lte=todays_date)
    finalrep = {}

    def get_sources(income):
        return income.source

    source_list = list(set(map(get_sources,incomes)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount

    for x in incomes:   
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)

    # return in json response 
    return JsonResponse({'income_source_data':finalrep},safe=False)
    
        




def income_stats_view(request):
    return render(request,'income/stats.html')


