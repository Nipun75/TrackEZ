from django.contrib.auth.models import User
from django.db import models
class Transaction(models.Model):
    INCOME='income'; EXPENSE='expense'
    TYPE_CHOICES=[(INCOME,'Income'),(EXPENSE,'Expense')]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='transactions')
    title=models.CharField(max_length=120)
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    transaction_type=models.CharField(max_length=10,choices=TYPE_CHOICES)
    date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-date','-created_at']
    def __str__(self): return f'{self.title} - {self.amount}'
