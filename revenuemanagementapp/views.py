from datetime import date, datetime, timedelta

from django import forms
from django.db.models import Q
from django.db.models.query import QuerySet
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from rest_framework import permissions ,status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from revenuemanagementapp.models import Income, Expense
from revenuemanagementapp.serializers import IncomeSerializer, ExpenseSerializer
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def home(request):
    return redirect(show_incomes)


@login_required(login_url='/sign-in/')
def show_incomes(request):
    return render(request, 'income.html')


@login_required(login_url='/sign-in/')
def show_expenses(request):
    return render(request, 'expense.html')


@login_required(login_url='/sign-in/')
def show_incomes_expenses(request):
    return render(request, 'income_expense.html')


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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Expense.objects.order_by("-id")[:20]

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
    permission_classes = [permissions.IsAuthenticated]

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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_receivers_senders_addresses(request, _type):
    if _type == "incomes":
        data = Income.objects.values_list('receiver', 'sender', 'address').distinct()
    else:
        data = Expense.objects.values_list('receiver', 'sender', 'address').distinct()
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def income_search(request):
    queries = []
    account = request.GET.get('account')
    amount = request.GET.get('amount')
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    month = request.GET.get('month')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if account:
        queries.append(Q(account=account))
    if amount:
        queries.append(Q(amount=amount))
    if sender:
        queries.append(Q(sender=sender))
    if receiver:
        queries.append(Q(receiver=receiver))
    if month:
        queries.append(Q(created_at__month=month, created_at__year=date.today().year))
    elif from_date and to_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        queries.append(Q(created_at__range=[from_date, to_date + timedelta(days=1)]))
    if queries:
        result = Income.objects.filter(*queries).order_by('-id').values()
        return Response(result)
    else:
        return Response()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def expense_search(request):
    queries = []
    account = request.GET.get('account')
    amount = request.GET.get('amount')
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    month = request.GET.get('month')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if account:
        queries.append(Q(account=account))
    if amount:
        queries.append(Q(amount=amount))
    if sender:
        queries.append(Q(sender=sender))
    if receiver:
        queries.append(Q(receiver=receiver))
    if month:
        queries.append(Q(created_at__month=month, created_at__year=date.today().year))
    elif from_date and to_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        queries.append(Q(created_at__range=[from_date, to_date + timedelta(days=1)]))
    if queries:
        result = Expense.objects.filter(*queries).order_by('-id').values()
        return Response(result)
    else:
        return Response()
