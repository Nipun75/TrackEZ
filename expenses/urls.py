from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('income/add/', views.add_income, name='add_income'),
    path('expense/add/', views.add_expense, name='add_expense'),
    path('transactions/', views.history, name='history'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    path('export/', views.export_transactions, name='export'),
    path('quick/', views.quick_transaction, name='quick'),
    path('budgets/', views.budget_list, name='budgets'),
    path('budgets/<int:pk>/delete/', views.delete_budget, name='delete_budget'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),
]