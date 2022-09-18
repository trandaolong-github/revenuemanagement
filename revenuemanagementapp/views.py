from django import forms
from django.db.models.query import QuerySet
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from revenuemanagementapp.models import Income, Expense
from revenuemanagementapp.serializers import IncomeSerializer, ExpenseSerializer
from revenuemanagementapp.forms import CreateExpenseForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def home(request):
    return redirect(show_incomes)

@login_required(login_url='/sign-in/')
def show_incomes(request):
    return render(request, 'income.html')

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


class IncomeList(GenericAPIView):

    serializer_class = IncomeSerializer

    def get_queryset(self) -> QuerySet:
        return Income.objects.order_by("-id")[:20]

    def get(self, request: Request, format=None) -> Response:
        """
        List all income instances
        """

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None) -> Response:
        """
        Create a new income instance
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IncomeDetail(GenericAPIView):

    serializer_class = IncomeSerializer

    def get_object(self) -> Income:
        obj = get_object_or_404(Income, id=self.kwargs["pk"])
        return obj

    def get(self, request: Request, pk: int, format=None) -> Response:
        """
        Retrieve an income instance
        """

        income = self.get_object()
        serializer = self.serializer_class(income)
        return Response(serializer.data)

    def put(self, request: Request, pk: int, format=None) -> Response:
        """
        Update an income instance
        """

        income = self.get_object()
        serializer = self.serializer_class(income, data=request.data)
        serializer.is_valid(raise_exception=True)
        income = serializer.save()
        return Response(serializer.data)


class ExpenseList(GenericAPIView):

    serializer_class = ExpenseSerializer

    def get_queryset(self) -> QuerySet:
        return Expense.objects.all()

    def get(self, request: Request, format=None) -> Response:
        """
        List all expense instances
        """

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None) -> Response:
        """
        Create a new expense instance
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExpenseDetail(GenericAPIView):

    serializer_class = ExpenseSerializer

    def get_object(self) -> Expense:
        obj = get_object_or_404(Expense, id=self.kwargs["pk"])
        return obj

    def get(self, request: Request, pk: int, format=None) -> Response:
        """
        Retrieve an expense instance
        """

        expense = self.get_object()
        serializer = self.serializer_class(expense)
        return Response(serializer.data)

    def put(self, request: Request, pk: int, format=None) -> Response:
        """
        Update an expense instance
        """

        expense = self.get_object()
        serializer = self.serializer_class(expense, data=request.data)
        serializer.is_valid(raise_exception=True)
        expense = serializer.save()
        return Response(serializer.data)
