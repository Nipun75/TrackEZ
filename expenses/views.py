import json
from datetime import date
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from .forms import RegisterForm, TransactionForm
from .models import Transaction

def register(request):
    if request.user.is_authenticated: return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(); login(request, user); messages.success(request, "Account created successfully."); return redirect("dashboard")
    return render(request, "register.html", {"form": form})

@login_required
def dashboard(request):
    qs = Transaction.objects.filter(user=request.user)
    income = sum((x.amount for x in qs if x.transaction_type == Transaction.INCOME), Decimal("0"))
    expense = sum((x.amount for x in qs if x.transaction_type == Transaction.EXPENSE), Decimal("0"))
    dates = sorted({x.date.isoformat() for x in qs})
    income_by_date = {d: sum((x.amount for x in qs if x.date.isoformat() == d and x.transaction_type == Transaction.INCOME), Decimal("0")) for d in dates}
    expense_by_date = {d: sum((x.amount for x in qs if x.date.isoformat() == d and x.transaction_type == Transaction.EXPENSE), Decimal("0")) for d in dates}
    top_expenses = qs.filter(transaction_type=Transaction.EXPENSE).order_by("-amount")[:5]
    top_income = qs.filter(transaction_type=Transaction.INCOME).order_by("-amount")[:5]
    return render(request, "dashboard.html", {
        "income": income, "expense": expense, "balance": income - expense, "recent": qs[:5],
        "labels_json": json.dumps(dates),
        "income_data_json": json.dumps([float(income_by_date[d]) for d in dates]),
        "expense_data_json": json.dumps([float(expense_by_date[d]) for d in dates]),
        "top_expense_labels_json": json.dumps([x.title for x in top_expenses]),
        "top_expense_data_json": json.dumps([float(x.amount) for x in top_expenses]),
        "top_income_labels_json": json.dumps([x.title for x in top_income]),
        "top_income_data_json": json.dumps([float(x.amount) for x in top_income]),
    })

@login_required
def add_income(request): return transaction_form(request, Transaction.INCOME)

@login_required
def add_expense(request): return transaction_form(request, Transaction.EXPENSE)

def transaction_form(request, kind):
    form = TransactionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False); obj.user = request.user; obj.transaction_type = kind; obj.save()
        messages.success(request, f"{kind.title()} added successfully."); return redirect("dashboard")
    return render(request, "transaction_form.html", {"form": form, "kind": kind.title()})

@login_required
def history(request):
    qs = Transaction.objects.filter(user=request.user)
    start_date, end_date = request.GET.get("start", ""), request.GET.get("end", "")
    if start_date:
        try: qs = qs.filter(date__gte=date.fromisoformat(start_date))
        except ValueError: messages.error(request, "Invalid start date."); start_date = ""
    if end_date:
        try: qs = qs.filter(date__lte=date.fromisoformat(end_date))
        except ValueError: messages.error(request, "Invalid end date."); end_date = ""
    return render(request, "history.html", {"transactions": qs, "start_date": start_date, "end_date": end_date})

@login_required
def delete_transaction(request, pk):
    obj = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST": obj.delete(); messages.success(request, "Transaction deleted.")
    return redirect("history")

@login_required
def export_transactions(request):
    qs = Transaction.objects.filter(user=request.user)
    for key, lookup in (("start", "date__gte"), ("end", "date__lte")):
        value = request.GET.get(key)
        if value:
            try: qs = qs.filter(**{lookup: date.fromisoformat(value)})
            except ValueError: return HttpResponse(f"Invalid {key} date.", status=400)
    workbook = Workbook(); sheet = workbook.active; sheet.title = "Transactions"
    headers = ["Title", "Amount", "Type", "Date"]; sheet.append(headers)
    for cell in sheet[1]: cell.font = Font(bold=True)
    for t in qs: sheet.append([t.title, float(t.amount), t.get_transaction_type_display(), t.date])
    for i, width in enumerate([28, 16, 16, 16], 1): sheet.column_dimensions[get_column_letter(i)].width = width
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="trackez_transactions.xlsx"'; workbook.save(response); return response

@login_required
def quick_transaction(request):
    result = None
    if request.method == "POST":
        try:
            income = Decimal(request.POST.get("income", "0") or "0")
            expenses = sum((Decimal(x or "0") for x in request.POST.getlist("expense")), Decimal("0"))
            result = income - expenses
        except InvalidOperation: messages.error(request, "Please enter valid numbers.")
    return render(request, "quick.html", {"result": result})
