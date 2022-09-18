from datetime import date

from django.db import models
from django.utils import timezone


class Income(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=200)
    amount  = models.CharField(max_length=20)
    account = models.CharField(max_length=100)
    income_type = models.CharField(max_length=100)
    accounting_voucher = models.CharField(max_length=100)
    receiving_date = models.DateField(default=date.today)
    receiver = models.CharField(max_length=100)

    sender = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    place = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)


class Expense(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=200)
    amount  = models.CharField(max_length=20)
    account = models.CharField(max_length=100)
    expense_type = models.CharField(max_length=100)
    accounting_voucher = models.CharField(max_length=100)
    budget = models.CharField(max_length=100)
    contract = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)

    applicant = models.CharField(max_length=100)
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)
