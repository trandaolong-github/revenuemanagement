from django import forms
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from revenuemanagementapp.models import Income, Expense
from revenuemanagementapp.forms import CreateIncomeForm, CreateExpenseForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def home(request):
    return redirect(show_incomes)

@login_required(login_url='/sign-in/')
def create_income(request):
    create_income_form = CreateIncomeForm()
    if request.method == "POST":
        create_income_form = CreateIncomeForm(request.POST)
        if create_income_form.is_valid():
            new_income = create_income_form.save(commit=False)
            new_income.save()

            return redirect(show_incomes)
    return render(request, 'create_income.html', {'create_income_form': create_income_form})

@login_required(login_url='/sign-in/')
def show_incomes(request):
    if request.user.is_superuser:
        incomes = Income.objects.order_by("-id").values()
        return render(request, 'income_admin.html', {"incomes": list(incomes)})

    incomes = Income.objects.order_by("-id")[:10]
    return render(request, 'income.html', {"incomes": incomes})

@login_required(login_url='/sign-in/')
@user_passes_test(lambda u:u.is_superuser, login_url='/')
def edit_income(request, income_id):
    income = Income.objects.get(id=income_id)

    if request.method == "POST":
        form = CreateIncomeForm(request.POST, request.FILES, instance=income)
        if form.is_valid():
            form.save()
            return redirect(show_incomes)
    else:
        form = CreateIncomeForm(instance=income)

    return render(request, 'edit_income.html', {"form": form})

@login_required(login_url='/sign-in/')
def create_expense(request):
    create_expense_form = CreateExpenseForm()
    if request.method == "POST":
        create_expense_form = CreateExpenseForm(request.POST)
        if create_expense_form.is_valid():
            new_income = create_expense_form.save(commit=False)
            new_income.save()

            return redirect(show_expenses)
    return render(request, 'create_expense.html', {'create_expense_form': create_expense_form})

@login_required(login_url='/sign-in/')
def show_expenses(request):
    if request.user.is_superuser:
        expenses = Expense.objects.order_by("-id").values()
        return render(request, 'expense_admin.html', {"expenses": list(expenses)})

    expenses = Expense.objects.order_by("-id")[:10]
    return render(request, 'expense.html', {"expenses": expenses})

@login_required(login_url='/sign-in/')
@user_passes_test(lambda u:u.is_superuser, login_url='/')
def edit_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)

    if request.method == "POST":
        form = CreateExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            return redirect(show_expenses)
    else:
        form = CreateExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {"form": form})

@login_required(login_url='/sign-in/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(change_password)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

@login_required(login_url='/sign-in/')
@user_passes_test(lambda u:u.is_superuser, login_url='/')
def management_home(request):
    return render(request, 'management/base_management.html')

@login_required(login_url='/sign-in/')
@user_passes_test(lambda u:u.is_superuser, login_url='/')
def management_report(request):
    return render(request, 'management/report.html')
