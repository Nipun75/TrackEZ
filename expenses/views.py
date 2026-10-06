from datetime import date
from decimal import Decimal,InvalidOperation
import csv
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,redirect,render
from .forms import RegisterForm,TransactionForm
from .models import Transaction

def register(request):
    if request.user.is_authenticated:return redirect('dashboard')
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save();login(request,user);return redirect('dashboard')
    return render(request,'register.html',{'form':form})
@login_required
def dashboard(request):
    qs=Transaction.objects.filter(user=request.user)
    income=sum((x.amount for x in qs if x.transaction_type==Transaction.INCOME),Decimal('0'))
    expense=sum((x.amount for x in qs if x.transaction_type==Transaction.EXPENSE),Decimal('0'))
    labels=sorted({x.date.isoformat() for x in qs})
    income_data=[float(sum((x.amount for x in qs if x.date.isoformat()==d and x.transaction_type==Transaction.INCOME),Decimal('0'))) for d in labels]
    expense_data=[float(sum((x.amount for x in qs if x.date.isoformat()==d and x.transaction_type==Transaction.EXPENSE),Decimal('0'))) for d in labels]
    return render(request,'dashboard.html',{'income':income,'expense':expense,'balance':income-expense,'recent':qs[:5],'labels':labels,'income_data':income_data,'expense_data':expense_data})
@login_required
def add_income(request): return transaction_form(request,Transaction.INCOME)
@login_required
def add_expense(request): return transaction_form(request,Transaction.EXPENSE)
def transaction_form(request,kind):
    form=TransactionForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False);obj.user=request.user;obj.transaction_type=kind;obj.save();messages.success(request,f'{kind.title()} added successfully.');return redirect('dashboard')
    return render(request,'transaction_form.html',{'form':form,'kind':kind.title()})
@login_required
def history(request): return render(request,'history.html',{'transactions':Transaction.objects.filter(user=request.user)})
@login_required
def delete_transaction(request,pk):
    obj=get_object_or_404(Transaction,pk=pk,user=request.user)
    if request.method=='POST':obj.delete();messages.success(request,'Transaction deleted.')
    return redirect('history')
@login_required
def export_transactions(request):
    qs=Transaction.objects.filter(user=request.user)
    response=HttpResponse(content_type='text/csv');response['Content-Disposition']='attachment; filename="trackez_transactions.csv"'
    writer=csv.writer(response);writer.writerow(['Title','Amount','Type','Date'])
    for t in qs:writer.writerow([t.title,t.amount,t.get_transaction_type_display(),t.date])
    return response
@login_required
def quick_transaction(request):
    result=None
    if request.method=='POST':
        try: result=Decimal(request.POST.get('income','0') or '0')-sum((Decimal(x or '0') for x in request.POST.getlist('expense')),Decimal('0'))
        except InvalidOperation:messages.error(request,'Please enter valid numbers.')
    return render(request,'quick.html',{'result':result})
