from django.contrib.auth.models import User
from django.db import models

class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [(INCOME, 'Income'), (EXPENSE, 'Expense')]

    FOOD = 'Food'
    TRAVEL = 'Travel'
    SHOPPING = 'Shopping'
    BILLS = 'Bills'
    EDUCATION = 'Education'
    HEALTH = 'Health'
    ENTERTAINMENT = 'Entertainment'
    OTHER = 'Other'
    CATEGORY_CHOICES = [
        (FOOD, 'Food'), (TRAVEL, 'Travel'), (SHOPPING, 'Shopping'),
        (BILLS, 'Bills'), (EDUCATION, 'Education'), (HEALTH, 'Health'),
        (ENTERTAINMENT, 'Entertainment'), (OTHER, 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default=OTHER)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.title} - {self.amount}'


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    month = models.DateField(help_text='Use the first day of the month.')
    category = models.CharField(max_length=30, choices=Transaction.CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-month', 'category']
        constraints = [
            models.UniqueConstraint(fields=['user', 'month', 'category'], name='unique_user_month_category_budget')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.category} - {self.month:%Y-%m}'

    @property
    def month_label(self):
        return self.month.strftime('%B %Y')
