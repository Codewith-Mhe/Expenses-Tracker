from django.shortcuts import render, redirect
from .form import ExpenseForm
from .models import Expense
from datetime import date, timedelta
from django.db.models import Sum as sum

def index(request):
    if request.method == 'POST':
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
    expenses = Expense.objects.all()  
    total_expense = expenses.aggregate(sum('amount'))
    
    ##calculating 365 days expenses
    last_year = date.today() - timedelta(365)
    data = Expense.objects.filter(date__gt = last_year)
    yearly_sum = data.aggregate(sum('amount'))
    

    ##calculating monthly expenses
    last_month = date.today() - timedelta(30)
    data = Expense.objects.filter(date__gt = last_month)
    monthly_sum = data.aggregate(sum('amount'))
    

    ##calculating weekly expenses
    weekly = date.today() - timedelta(7)
    data = Expense.objects.filter(date__gt = weekly)
    weekly_sum = data.aggregate(sum('amount'))
    
    ##daily expenses
    daily_sum = Expense.objects.filter().values('date').order_by('date').annotate(sum=sum('amount'))

    categories_sum = Expense.objects.filter().values('category').order_by('category').annotate(sum=sum('amount'))
    
    expense_form = ExpenseForm 
    return render(request, 'myapp/index.html', {'expense_form':expense_form, 'expenses':expenses, 'total_expense':total_expense, 'yearly_sum':yearly_sum, 'monthly_sum':monthly_sum, 'weekly_sum':weekly_sum, 'daily_sum':daily_sum, 'categories_sum':categories_sum})

def edit(request, id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    expense = Expense.objects.get(id=id)
    form = ExpenseForm(request.POST, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'myapp/edit.html', {'expense_form':expense_form})

def delete(request, id):
    if request.method =="POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')

