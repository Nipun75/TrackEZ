from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Budget, Transaction

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('title', 'amount', 'category', 'date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Grocery shopping'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 2:
            raise ValidationError('Title must contain at least 2 characters.')
        return title

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
        return amount

    def clean_date(self):
        value = self.cleaned_data['date']
        if value > timezone.localdate():
            raise ValidationError('Transaction date cannot be in the future.')
        return value

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ('month', 'category', 'amount')
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError('Budget amount must be greater than zero.')
        return amount

    def clean_month(self):
        value = self.cleaned_data['month']
        return value.replace(day=1)
