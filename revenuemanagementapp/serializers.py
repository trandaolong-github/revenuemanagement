from django.db import transaction
from rest_framework import serializers

from revenuemanagementapp import models


class IncomeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    class Meta:
        model = models.Income
        fields = (
            'id',
            'created_at',
            'content',
            'amount',
            'account',
            'income_type',
            'accounting_voucher',
            'budget',
            'contract',
            'branch',
            'applicant',
            'company',
            'address',
        )

    @transaction.atomic
    def create(self, validated_data):
        income = models.Income.objects.create(**validated_data)
        return income

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.account = validated_data.get("account", instance.account)
        instance.income_type = validated_data.get("income_type", instance.income_type)
        instance.accounting_voucher = validated_data.get("accounting_voucher", instance.accounting_voucher)
        instance.budget = validated_data.get("budget", instance.budget)
        instance.contract = validated_data.get("contract", instance.contract)
        instance.branch = validated_data.get("branch", instance.branch)
        instance.applicant = validated_data.get("applicant", instance.applicant)
        instance.company = validated_data.get("company", instance.company)
        instance.address = validated_data.get("address", instance.address)

        instance.save()
        return instance


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expense
        fields = (
            'content',
            'amount',
            'account',
            'expense_type',
            'accounting_voucher',
            'budget',
            'contract',
            'branch',
            'applicant',
            'company',
            'address',
        )

    @transaction.atomic
    def create(self, validated_data):
        expense = models.Expense.objects.create(**validated_data)
        return expense

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.account = validated_data.get("account", instance.account)
        instance.expense_type = validated_data.get("expense_type", instance.expense_type)
        instance.accounting_voucher = validated_data.get("accounting_voucher", instance.accounting_voucher)
        instance.budget = validated_data.get("budget", instance.budget)
        instance.contract = validated_data.get("contract", instance.contract)
        instance.branch = validated_data.get("branch", instance.branch)
        instance.applicant = validated_data.get("applicant", instance.applicant)
        instance.company = validated_data.get("company", instance.company)
        instance.address = validated_data.get("address", instance.address)

        instance.save()
        return instance
