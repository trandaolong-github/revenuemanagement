from datetime import date

from django.db import transaction
from rest_framework import serializers

from revenuemanagementapp import models


class IncomeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    receiving_date = serializers.DateField(required=False)
    accounting_voucher = serializers.CharField(required=False, max_length=20)
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
            'receiving_date',
            'receiver',
            'sender',
            'address',
            'place',
        )

    @transaction.atomic
    def create(self, validated_data):
        income = models.Income.objects.create(**validated_data)
        income.accounting_voucher = "T" + str(income.id) + "/" + str(date.today().month) + "/" + str(date.today().year)
        income.save()
        return income

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.account = validated_data.get("account", instance.account)
        instance.income_type = validated_data.get("income_type", instance.income_type)
        instance.accounting_voucher = validated_data.get("accounting_voucher", instance.accounting_voucher)
        instance.receiving_date = validated_data.get("receiving_date", instance.receiving_date)
        instance.receiver = validated_data.get("receiver", instance.receiver)
        instance.sender = validated_data.get("sender", instance.sender)
        instance.address = validated_data.get("address", instance.address)
        instance.place = validated_data.get("place", instance.place)

        instance.save()
        return instance


class ExpenseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    sending_date = serializers.DateField(required=False)
    accounting_voucher = serializers.CharField(required=False, max_length=20)
    class Meta:
        model = models.Expense
        fields = (
            'id',
            'created_at',
            'content',
            'amount',
            'account',
            'expense_type',
            'accounting_voucher',
            'sending_date',
            'sender',
            'receiver',
            'address',
            'place',
        )

    @transaction.atomic
    def create(self, validated_data):
        expense = models.Expense.objects.create(**validated_data)
        expense.accounting_voucher = "C" + str(expense.id) + "/" + str(date.today().month) + "/" + str(date.today().year)
        expense.save()
        return expense

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.account = validated_data.get("account", instance.account)
        instance.expense_type = validated_data.get("expense_type", instance.expense_type)
        instance.accounting_voucher = validated_data.get("accounting_voucher", instance.accounting_voucher)
        instance.sending_date = validated_data.get("sending_date", instance.sending_date)
        instance.sender = validated_data.get("sender", instance.sender)
        instance.receiver = validated_data.get("receiver", instance.receiver)
        instance.address = validated_data.get("address", instance.address)
        instance.place = validated_data.get("place", instance.place)

        instance.save()
        return instance
